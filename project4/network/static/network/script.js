// Get dialog and add open, close and submit actions
const dialog = document.querySelector('dialog');

if (document.querySelector('#new-post') != null) {
    document.querySelector('#new-post').onclick = () => {
        document.querySelector('textarea').value = '';
        document.querySelector('form').action = '/add-post';
        document.querySelector('#submit').type = "submit";
        document.querySelector('#submit').innerHTML = 'Post';
        dialog.showModal();
    }
    document.querySelector('#cancel-new-post').onclick = () => {
        dialog.close();
    }
    document.querySelector('#form-new-post').onsubmit = () => {
        dialog.close();
    };
}


const editBtns = document.querySelectorAll('#edit');
editBtns.forEach(btn => {
    btn.addEventListener('click', getPost)
});

let fetchFunction;

function getPost (event) {
    dialog.showModal(); 
    const postId = event.target.parentNode.id
    const submitBtn = document.querySelector('#submit');
    submitBtn.type = "button";
    submitBtn.innerHTML = 'Edit';
    const postContent = document.querySelector("#"+CSS.escape(postId)+" .post-content");
    const textArea = document.querySelector('textarea');
    const postTime = document.querySelector("#"+CSS.escape(postId)+" .time");
    textArea.value = postContent.textContent;
    textArea.selectionStart = textArea.value.length;
    textArea.selectionEnd = textArea.value.length;
    fetchFunction = () => {
        fetchPost(postContent, postId, postTime);
    }
    submitBtn.addEventListener('click', fetchFunction);
    
}

function fetchPost (post, postId, postTime) {
    document.querySelector('#submit').removeEventListener('click', fetchFunction)
    const content = document.querySelector('textarea').value;
    fetch(`/post${postId}/edit`, {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
    });
    updateDom(post,postTime,content)
    dialog.close();
}

function updateDom (post, postTime,content) {
    const date = new Date();
    const options = {month:"long",
    day:"numeric",
    year:"numeric",
    hour:"numeric",
    minute:"2-digit",
    timeZone:"utc"}
    postTime.textContent = date.toLocaleString("en-US", options)
                                .replace(" at", ",")
                                .replace("AM","a.m.")
                                .replace("PM", "p.m.")
    post.textContent = content;
    const allPosts = post.parentNode.parentNode;
    allPosts.prepend(post.parentNode);
    post.parentNode.scrollIntoView({behavior: 'smooth'});
}

if (document.querySelector("#loged-user") != null) {
    const likeBtn = document.querySelectorAll('#like');
    likeBtn.forEach(btn => {
        btn.addEventListener('click', (event) => {
            const postId = event.target.closest(".post").id;
            likePost(postId);
            btn.classList.toggle("liked");
            btn.classList.toggle("not-liked");
            const likesCount = btn.querySelector("span");
            if (btn.classList.contains("liked")) {
                likesCount.textContent = parseInt(likesCount.textContent)+1
            } else {
                likesCount.textContent = parseInt(likesCount.textContent)-1
            }
        })
    });
}

function likePost (postId) {
    fetch(`/post${postId}/like`, {method:"POST"});
}

if (document.querySelector("#follow") != null) {
    const followBtn = document.querySelector("#follow");
    followBtn.addEventListener('click', () => {
        const pageUser = window.location.pathname;
        fetch(`${pageUser}/folow`, {method:"POST"});
        const followersField = document.querySelector(".followers span");
        if (followBtn.classList.contains("Follow")) {
            followBtn.textContent = "Unfollow";
            followersField.textContent = parseInt(followersField.textContent)+1;
            console.log()
        } else {
            followBtn.textContent = "Follow";
            followersField.textContent = parseInt(followersField.textContent)-1;
        }
        followBtn.classList.toggle("Follow");
        followBtn.classList.toggle("Unfollow");
    })
}
