import "./web-components/post-element.js";

export function togglePostButton(postText, postButton, previewImage) {
    if (postText.value.trim() !== '' || previewImage.src !== "") {
        postButton.disabled = false; // Enable button
    } else {
        postButton.disabled = true; // Disable button
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    // Check empty new post
    const postText = document.querySelector("#new-post-textarea");
    const postImage = document.querySelector("#postImage");
    const previewImage = document.querySelector("#previewImage");
    const postButton = document.querySelector("#post-button")
    postText.addEventListener('input', () => {
        togglePostButton(postText, postButton, previewImage);
    });
    postImage.addEventListener('change', () => {
        togglePostButton(postText, postButton, previewImage);
    });
    togglePostButton(postText, postButton, previewImage);

    // Query elements
    const createPostForm = document.getElementById('create-post-form');
    const postsContainer = document.getElementById('posts-container');

    // fetch posts when the page loads
    // then render each post using the post-element web component
    const posts = await fetchPosts();
    posts.forEach(post => {
        const postElement = document.createElement('post-element');
        postElement.postID = post.postID;
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
            postElement.postID = post.postID;
            postElement.user = post.user;
            postElement.content = post.content;
            postElement.image = post.image;
            postElement.createdAt = new Date(post.created_at);
            const postsContainer = document.getElementById('posts-container');
            postsContainer.prepend(postElement);
            createPostForm.reset();
            document.querySelector('#preview-image-container').style.display = 'none';
            postButton.disabled = true;
        }
    })

    document.getElementById('postImage').addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const previewImage = document.getElementById('previewImage');
                previewImage.src = e.target.result;
                document.getElementById('preview-image-container').style.display = 'block';
            };

            reader.readAsDataURL(file);
        }
    });

    document.getElementById('postImageUpdate').addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const previewImage = document.getElementById('previewImageUpdate');
                previewImage.src = e.target.result;
                document.getElementById('preview-image-container-update').style.display = 'block';
            };

            reader.readAsDataURL(file);
        }
    });

    document.querySelector('.remove-image-post').addEventListener('click', () => {
        document.getElementById('preview-image-container').style.display = "none";
        document.getElementById('previewImage').removeAttribute("src");
        togglePostButton(postText, postButton, previewImage);
    })
});


async function fetchPosts() {
    const response = await fetch("/posts");
    return await response.json();
}





