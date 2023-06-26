function profile_info(username) {
    return window.location.replace(`/profile/${username}`);
}

function logout() {
    return window.location.replace('/accounts/logout');
}

function successResult(data) {
    $('#place').html(`<p style="color: limegreen">${data.answer}`)
  };

  function errorResult(data) {
      text = JSON.parse(data.responseText);
      const answer = `<span style="color:red">${text.error}</span>`;
      $('#place').html(answer);
};

function callEditProfileModal() {
    $('#edit_profile_modal').modal('show');
}

function callAddResumeModal() {
    $('#add_resume_modal').modal('show');
}

function editProfile(username) {
    let data = new FormData();
    data.append('first_name', document.getElementById('inputFirstName').value);
    data.append('last_name', document.getElementById('inputLastName').value);
    data.append('birthday_date', document.getElementById('inputBirthdayDate').value);
    data.append('address', document.getElementById('inputAddress').value);
    data.append('email', document.getElementById('inputEmailAddress').value);
    data.append('my_phone', document.getElementById('inputMyPhone').value);
    data.append('home_phone', document.getElementById('inputHomePhone').value);

    fetch("/profile/edit", {
        method: "POST",
        body: data,
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": $.cookie("csrftoken"),
        },
      }).then(function (response) {
        response.json().then(
            function (data) {
                if (data['response']) {
                    return window.location.replace(`/profile/${username}`);
                }
            }
        )
      })
}

function addResume(username) {
    let data = new FormData();
    let resume_description = document.getElementById('resume-description').value;
    if (!resume_description) {
        return alert('Нужно заполнить описание!');
    }else {
        data.append('description', resume_description);
        fetch("/profile/add_resume", {
            method: "POST",
            body: data,
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken"),
            },
          }).then(function (response) {
            response.json().then(
                function (data) {
                    if (data['response']) {
                        return window.location.replace(`/profile/${username}`);
                    }
                }
            )
          })
    }
}
