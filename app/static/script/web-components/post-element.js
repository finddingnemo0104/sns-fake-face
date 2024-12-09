import {LitElement, html, render} from '../lib/lit-core.min.js';
import {togglePostButton} from "../posts.js";

export class PostElement extends LitElement {
    static properties() {
        return {
            postID: {type: Number},
            user: {
                type: {
                    id: {type: Number},
                    name: {type: String}
                }
            },
            content: {type: String},
            image: {type: String},
            createdAt: {type: Date},
        };
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

        if (data.image !=="") {
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


    render() {
        return html`
            <div class="post">
                <div class="d-flex align-items-center mb-2">
                    <img src="https://via.placeholder.com/40" class="rounded-circle" alt="User Image">
                    <div class="ms-2 m-0">
                        <div class="fw-bold">${this.user.name}</div>
                        <div class="text-secondary">${this.createdAt.toLocaleDateString()} at
                            ${this.createdAt.toLocaleTimeString()}
                        </div>
                    </div>

                    <div class="dropdown ms-auto">
                        <i class="bi bi-three-dots ms-auto post-management" role="button" data-bs-toggle="dropdown"
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
                    </div>
                </div>

                <p>${this.content}</p>

                ${
                        this.image ? html`<img src="${this.image}" class="img-fluid mb-2 w-100 h-auto"
                                               alt="Post Image">` : ''
                }

                <!-- Comment Section -->
                <div class="comment-section mt-3">
                    <textarea class="form-control mb-2" rows="2" placeholder="Write a comment..."
                              style="resize: none"></textarea>
                    <button class="btn btn-primary btn-sm">Comment</button>
                </div>
            </div>`;
    }

    createRenderRoot() {
        return this;
    }
}

customElements.define('post-element', PostElement);
