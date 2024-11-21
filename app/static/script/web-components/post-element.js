import {LitElement, html, render } from '../lib/lit-core.min.js';

export class PostElement extends LitElement {
    static properties() {
        return {
            user: {type: {
                id: {type: Number},
                name: {type: String}
            }},
            content: {type: String},
            image: {type: String},
            createdAt: {type: Date},
        };
    }

    render() {

        return html`
            <div class="post">
                <div class="d-flex align-items-center mb-2">
                    <img src="https://via.placeholder.com/40" class="rounded-circle" alt="User Image">
                    <div class="ms-2 m-0">
                        <div class="fw-bold">${this.user.name}</div>
                        <div class="text-secondary">${this.createdAt.toLocaleDateString()} at ${this.createdAt.toLocaleTimeString()}</div>
                    </div>
                </div>
                
                <p>${this.content}</p>

                ${
                    this.image ? html`<img src="${this.image}" class="img-fluid mb-2 w-100 h-auto" alt="Post Image">` : ''
                }
                
                <!-- Comment Section -->
                <div class="comment-section mt-3">
                    <textarea class="form-control mb-2" rows="2" placeholder="Write a comment..."></textarea>
                    <button class="btn btn-primary btn-sm">Comment</button>
                </div>
            </div>`;
    }

    createRenderRoot() { return this;}
}
customElements.define('post-element', PostElement);
