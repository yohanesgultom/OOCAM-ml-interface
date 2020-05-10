const hideSourceInputs = (event) => {    
    document.querySelectorAll('.prediction-source-option').forEach((elm) => {
        elm.parentElement.style.display = (elm.name === event.target.value) ? 'block' : 'none';
    })    
}

document.querySelectorAll('input[name=source]').forEach((elm) => {
    elm.addEventListener('click', hideSourceInputs);
    if (elm.checked === true) {
        elm.click();
    }
})