// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// function handleFolderSelectChange() {
//     if (folderSelect.value === 'Create new folder') {
//       newFolderDiv.classList.remove('d-none');
//       createFolderButton.classList.remove('d-none');
//     } else {
//       newFolderDiv.classList.add('d-none');
//       createFolderButton.classList.add('d-none');
//       selectedFolderDeclare.textContent  = folderSelect.value;
//     }
//   }