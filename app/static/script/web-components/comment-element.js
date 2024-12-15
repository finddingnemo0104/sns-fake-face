import {LitElement, html, render} from '../lib/lit-core.min.js';

export class CommentElement extends LitElement {
    static properties() {
        return {
            commentID: {type: Number},
            content: {type: String},
            user: {
                type: {
                    id: {type: Number},
                    name: {type: String},
                    avatar: {type: String}
                }
            },
            postID: {type: Number},
            createAt: {type: Date},
            updateAt: {type: Date},
            isOwner: {type: Boolean}
        };
    }

    async deleteComment() {
        const response = await fetch(`/comments/delete/${this.commentID}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            this.remove()
        }
    }

    constructor() {
        super();
    }

    render() {
        return html`
            <div class="d-flex my-3">
                <img class="rounded-circle me-2 my-2" src="${this.user.avatar}" width="32" height="32"
                     alt="${this.user.name}"/>
                <div class="d-flex flex-column">
                    <div class="rounded-4 w-100 p-2 px-3" style="background-color: #e8e8e8">
                        <div class="d-flex flex-column">
                            <div class="d-flex">
                                <a href="/profile/${this.user.id}"
                                   class="text-primary text-decoration-none">${this.user.name}</a>
                                <span class="ms-2">${this.createAt.toLocaleDateString()}</span>

                            </div>
                            <div>${this.content}</div>
                        </div>
                    </div>
                    <div class="d-flex px-3">
                        <span>${this.createAt.toLocaleTimeString()}</span>
                        ${this.isOwner ? (
                                html`
                                    <button @click=${this.deleteComment} class="text-decoration-none btn py-0">
                                        Xoá
                                    </button>`
                        ) : ""}
                    </div>
                </div>
            </div>
        `;
    }

    createRenderRoot() {
        return this;
    }
}

customElements.define('comment-element', CommentElement);