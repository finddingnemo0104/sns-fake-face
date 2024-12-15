document.addEventListener('DOMContentLoaded', async function () {
    const sendFriendRequestButton = document.getElementById('send-friend-request');
    const rejectFriendRequestButton = document.getElementById("reject-friend-request");
    const editUserButton = document.getElementById('edit-user-button');
    if (sendFriendRequestButton) {
        sendFriendRequestButton.addEventListener('click', async () => {
            const response = await fetch(`/friend-request/${profileUserID}`, {
                method: 'POST',
            });

            if (response.ok) {
                const data = await response.json();
                sendFriendRequestButton.innerText = data.message;
            }
        });
    }

    editUserButton.addEventListener('click', async () => {
        const response = await fetch(`/users/detail/${profileUserID}`);
        const user = await response.json();

        const editFormContainer = document.querySelector('.list-group-flush');
        const html = `
                   <input type="date" class="form-control" name="dob" value="${new Date(user.dob).toISOString().split('T')[0]}"/>
                   <div class="form-floating mb-3">
                      <input name="email" type="email" class="form-control" id="floatingInput" placeholder="name@example.com" value="${user.email}">
                      <label for="floatingInput">Email</label>
                   </div>
                   <div class="form-floating">
                      <select required name="gender" class="form-select" id="floatingSelect" aria-label="Floating label select example">
                        <option value="Male" ${user.gender === 'Male' ? "selected" : ""}>Nam</option>
                        <option value="Female" ${user.gender === 'Female' ? "selected" : ""}>Nữ</option>
                        <option value="other" ${user.gender === 'other' ? "selected" : ""}>Khác</option>
                      </select>
                      <label for="floatingSelect">Works with selects</label>
                    </div>
                    <button class="btn btn-primary">
                        Xác nhận
</button>
                 
        `
        editFormContainer.innerHTML = html;
    })
});