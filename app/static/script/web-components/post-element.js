import {LitElement, html, render} from '../lib/lit-core.min.js';
import {togglePostButton} from "../posts.js";
import './comment-element.js';

export class PostElement extends LitElement {
    static properties() {
        return {
            postID: {type: Number},
            user: {
                type: {
                    id: {type: Number},
                    name: {type: String},
                    avatar: {type: String}
                }
            },
            content: {type: String},
            image: {type: String},
            createdAt: {type: Date},
            comments: {type: Array},
            totalLikes: {type: Number},
            liked: {type: Boolean},
            totalComments: {type: Number},
            isOwner: {type: Boolean}
        };
    }

    constructor() {
        super();
        this.comments = [];
        this.liked = false;
    }

    deletePost(postID) {
        document.querySelector("#delete-post").addEventListener('click', async () => {
            const response = await fetch(`/posts/delete/${postID}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (response.ok) {
                const modal = bootstrap.Modal.getInstance(document.querySelector("#confirm-delete-modal"));
                modal.hide();
                this.remove();
            }
        })
    }

    async updatePost(postID) {
        const response = await fetch(`/post/${postID}`, {
            method: 'GET'
        });
        const data = await response.json();
        const textPost = document.querySelector("#updated-post-textarea");
        const previewImageUpdate = document.querySelector("#previewImageUpdate");
        textPost.value = data.content;

        if (data.image !== "") {
            previewImageUpdate.src = data.image;
            document.querySelector("#preview-image-container-update").style.display = "block";
        }

        // Check empty update post
        const postTextUpdate = document.querySelector("#updated-post-textarea");
        const postImageUpdate = document.querySelector("#postImageUpdate");
        const postButtonUpdate = document.querySelector("#update-post-button")
        postTextUpdate.addEventListener('input', () => {
            togglePostButton(postTextUpdate, postButtonUpdate, previewImageUpdate);
        });
        postImageUpdate.addEventListener('change', () => {
            togglePostButton(postTextUpdate, postButtonUpdate, previewImageUpdate);
        });
        togglePostButton(postTextUpdate, postButtonUpdate, previewImageUpdate);

        document.querySelector('#remove-image-post-update').addEventListener('click', () => {
            document.getElementById('preview-image-container-update').style.display = "none";
            document.getElementById('previewImageUpdate').removeAttribute("src");
            togglePostButton(postTextUpdate, postButtonUpdate, previewImageUpdate);
        })

        // Save and display updated post
        document.querySelector('#update-post-button').addEventListener('click', async () => {
            const updatedContent = textPost.value;
            const updatedImage = postImageUpdate.files[0];  // Image to be updated

            const formData = new FormData();
            formData.append('content', updatedContent);
            if (updatedImage) {
                formData.append('image', updatedImage);
            }
            formData.append('previewImage', previewImageUpdate.src);

            const response = await fetch(`/post/update/${postID}`, {
                method: 'PATCH',
                body: formData,
            });

            if (response.ok) {
                const updatedPost = await response.json();
                this.content = updatedPost.content;
                this.image = updatedPost.image;
                this.requestUpdate();
                const modal = bootstrap.Modal.getInstance(document.querySelector("#update-post-modal"));
                modal.hide();
            }
        });
    };

    async sendComment(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        formData.append('postID', this.postID);
        const response = await fetch("/comments/create", {
            method: "POST",
            body: formData,
        });
        if (response.ok) {
            const commentData = await response.json();

            this.comments = [...this.comments, {
                ...commentData,
                createAt: new Date(commentData.create_at),
                updateAt: new Date(commentData.update_at),
                isOwner: true
            }]
            this.totalComments = commentData.totalComments;
            this.requestUpdate();
            form.reset()
        }
    }

    renderComment(comment) {
        return html`
            <comment-element
                    .commentID=${comment.commentID}
                    .content=${comment.content}
                    .user=${comment.user}
                    .postID=${comment.postID}
                    .createAt=${comment.createAt}
                    .updateAt=${comment.updateAt}
                    .isOwner=${comment.isOwner}
]            ></comment-element>
        `
    }

    renderComments() {
        if (window.location.href.includes("/detail")) {
            return this.comments.slice(0, 10).map((comment, index) => this.renderComment(comment))
        }
        return this.comments.slice(0, 2).map((comment, index) => this.renderComment(comment))
    }

    async handleLike() {
        const response = await fetch(`/posts/like/${this.postID}`);
        const data = await response.json();
        this.totalLikes = data.totalLikes;
        this.liked = data.liked;
        this.requestUpdate();
    }


    render() {
        return html`
            <div class="post">
                <div class="d-flex align-items-center mb-2">
                    <img src="${this.user.avatar}" width="32" height="32" class="rounded-circle" alt="User Image">
                    <div class="ms-2 m-0">
                        <a href="/profile/${this.user.id}" class="fw-bold text-decoration-none">${this.user.name}</a>
                        <div class="text-secondary">${this.createdAt.toLocaleDateString()} at
                            ${this.createdAt.toLocaleTimeString()}
                        </div>
                    </div>

                    ${this.isOwner ? (
                            html`
                                <div class="dropdown ms-auto">
                                    <i class="bi bi-three-dots ms-auto post-management" role="button"
                                       data-bs-toggle="dropdown"
                                       aria-expanded="false"></i>

                                    <ul class="dropdown-menu dropdown-menu-lg-end">
                                        <li>
                                            <button @click=${() => this.updatePost(this.postID)}
                                                    class="dropdown-item update-post" data-bs-toggle="modal"
                                                    data-bs-target="#update-post-modal">Chỉnh sửa bài viết
                                            </button>
                                        </li>
                                        <li>
                                            <button @click=${() => this.deletePost(this.postID)}
                                                    class="dropdown-item delete-post"
                                                    data-bs-toggle="modal"
                                                    data-bs-target="#confirm-delete-modal">Xóa
                                                bài viết
                                            </button>
                                        </li>
                                    </ul>
                                </div>`
                    ) : ""}
                </div>

                <p>${this.content}</p>

                ${
                        this.image ? html`<img src="${this.image}" class="img-fluid mb-2 w-100 h-auto"
                                               alt="Post Image">` : ''
                }

                <div class="w-100">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="bi bi-hand-thumbs-up-fill me-2 text-primary"></i>
                            ${this.totalLikes}
                        </div>
                        <div>
                            ${this.totalComments} bình luận
                        </div>
                    </div>
                    <div class="row border-top">
                        <button @click=${this.handleLike}
                                class="col-4 btn btn-light ${this.liked === true && 'text-primary'}">
                            <i class="bi bi-hand-thumbs-up-fill me-1"></i>
                            Thích
                        </button>
                        <a href="/posts/detail/${this.postID}" class="col-4 btn btn-light">
                            <i class="bi bi-chat me-1"></i>
                            Bình luận
                        </a>
                        <a class="col-4 btn btn-light"
                           type="button"
                           href="javascript:"
                           data-bs-toggle="modal"
                           data-bs-target="#copiedModal"
                           data-action="copy-link"
                           data-link="/posts/detail/${this.postID}">
                            <i class="fa-solid fa-link fa-xl text-dark text-decoration-none"></i>
                            Chia sẻ
                        </a>
                    </div>

                </div>

                <!-- Comment Section -->
                <div class="comment-section mt-3">
                    ${this.renderComments()}

                    <form @submit=${this.sendComment}>
                        <textarea name="content" class="form-control mb-2" rows="2"
                                  placeholder="Hãy chia sẻ ý kiến của bạn . . ."
                                  style="resize: none" required></textarea>
                        <button class="btn btn-primary btn-sm">Bình luận</button>
                    </form>

                </div>
            </div>`;
    }

    createRenderRoot() {
        return this;
    }
}

customElements.define('post-element', PostElement);
