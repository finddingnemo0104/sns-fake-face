import {LitElement, html, render} from '../lib/lit-core.min.js';

export class MessageElement extends LitElement {
    static properties() {
        return {
            message: {type: String},
            isSender: {type: Boolean},
            createAt: {type: String}
        };
    }

    constructor() {
        super();
        this.isSender = true;
        this.message = "A message";
    }

    render() {
        if (this.isSender) {
            return html`
            <div class="d-flex justify-content-end mb-2">
                <div class="d-flex flex-column">
                    <div class="bg-primary text-white p-2 rounded w-100">
                        ${this.message}
                    </div>
                    <div>
                        ${this.createAt}
                    </div>
                </div>
            </div>`;
        }
        return html`
        <div class="d-flex mb-2">
            <div class="d-flex flex-column mr-2">
                <div class="bg-light p-2 rounded w-100">${this.message}</div>
                       <div>
                        ${this.createAt}
                    </div>
            </div>
        </div>`;
    }

    createRenderRoot() { return this;}
}
customElements.define('message-element', MessageElement);