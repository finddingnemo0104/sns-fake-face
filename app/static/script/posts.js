import "./web-components/post-element.js";


document.addEventListener('DOMContentLoaded', async function () {
    // Query elements
    const createPostForm = document.getElementById('create-post-form');
    const postsContainer = document.getElementById('posts-container');

    // fetch posts when the page loads
    // then render each post using the post-element web component
    const posts = await fetchPosts();
    const postElements = posts.map(post => {
        const postElement = document.createElement('post-element');
        postElement.user = post.user;
        postElement.content = post.content;
        postElement.image = post.image;
        postElement.createdAt = new Date(post.created_at);
        postsContainer.appendChild(postElement);
    });


    // Event listener for submitting a post
    createPostForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(createPostForm);
        const image = createPostForm.querySelector('input[type="file"]').files[0];
        if (image) {
            formData.append('image', image);
        }

        const response = await fetch("/posts/create", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const post = await response.json();
            const postElement = document.createElement('post-element');
            postElement.user = post.user;
            postElement.content = post.content;
            postElement.image = post.image;
            postElement.createdAt = new Date(post.created_at);
            const postsContainer = document.getElementById('posts-container');
            postsContainer.prepend(postElement);
            createPostForm.reset();
        }
    })
});


async function fetchPosts() {
    const response = await fetch("/posts");
    return await response.json();
}