function formValidateFilledInputs(form) {
    let inputs = form.elements

    let errorMessage = '';

    for (let i = 0; i < inputs.length; i++) {
        let input = inputs[i];

        if (input.value == '' && input.type != 'submit') {
            errorMessage = 'Você precisa preencher todos os campos!'
        }

        if (errorMessage) {
            Swal.fire({
                'icon': 'error',
                confirmButtonColor: "#3085d6",
                text: errorMessage
            });

            return false;
        }

    }

    return true;

}

function formatPrecoInput(element){
    let value = element.value;
    const re = /[^0-9.]/g;
    value = value.replace(re, '');
    element.value = value;
}
