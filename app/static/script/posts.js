import "./web-components/post-element.js";

export function togglePostButton(postText, postButton, previewImage) {
    if (postText.value.trim() !== '' || previewImage.src !== "") {
        postButton.disabled = false; // Enable button
    } else {
        postButton.disabled = true; // Disable button
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    // Thêm sự kiện khi bấm nút chia sẻ trong post
    copyLinkToClipBoard('posts-container');

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
    // then render each post using the post-element web
    if (window.location.href.includes("/posts/detail")) {
        const postID = (location.pathname + location.search).substr(1).split("/detail/")[1]
        showPostByID(postID);
    } else {
        showPosts();
    }


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
            const postsContainer = document.getElementById('posts-container');
            postsContainer.prepend(createPostElement(post));
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

    async function showPosts() {
        let profileId = null;
        if (window.location.pathname.includes("/profile")) {
            profileId = profileUserID;
        }
        const posts = await fetchPosts(profileId);
        posts.forEach((post, index) => {
            postsContainer.appendChild(createPostElement(post));
        });
    }

    async function showPostByID(postID) {
        const response = await fetch(`/post/${postID}`)
        const post = await response.json();
        postsContainer.appendChild(createPostElement(post));

    }
});


async function fetchPosts(profileId) {
    const searchParams = new URLSearchParams({
        profileId: profileId
    })
    const response = await fetch(`/posts?${searchParams}`);
    const data = await response.json();
    return data.posts;
}

function createPostElement(post) {
    const postElement = document.createElement('post-element');
    postElement.postID = post.postID;
    postElement.user = post.user;
    postElement.content = post.content;
    postElement.image = post.image;
    postElement.createdAt = new Date(post.created_at);
    postElement.totalLikes = post.totalLikes;
    postElement.liked = post.liked;
    postElement.totalComments = post.totalComments;
    postElement.isOwner = post.isOwner;
    postElement.comments = post.comments.map((comment) => (
        {
            ...comment,
            createAt: new Date(comment.create_at),
            updateAt: new Date(comment.update_at),
        }
    ))
    return postElement;
}

// idParentNode: string. Example: "list-post"
function copyLinkToClipBoard(idParentNode) {
    document.getElementById(idParentNode).addEventListener('click', function (event) {
        let target = event.target; // where was the click?
        if (target.tagName !== 'A') return;
        if (target.dataset.action !== 'copy-link') return;
        let linkText = `${document.location.origin}${target.dataset.link}`;
        navigator.clipboard.writeText(linkText).then(function () {
            console.log('Async: Copying to clipboard was successful!');
        }, function (err) {
            console.error('Async: Could not copy text: ', err);
        });
    })
}