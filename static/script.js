experienceCurrentField = document.getElementById('id_current')
experienceEnddateField = document.getElementById('id_enddate')

// experienceCurrentField.addEventListener('change', alert("Toggled!"))
experienceCurrentField.addEventListener('change', experienceToggleCurrent)

function experienceToggleCurrent() {
    if (experienceCurrentField.checked) {
        experienceEnddateField.disabled = true;
        experienceEnddateField.style.display = 'none';
    }
    else {
        experienceEnddateField.disabled = false;
        experienceEnddateField.style.display = '';
    }
}