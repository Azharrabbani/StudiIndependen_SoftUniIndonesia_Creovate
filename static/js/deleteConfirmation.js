document.addEventListener('DOMContentLoaded', function(){
    const deleteModal = document.getElementById('delete-modal');
    let deleteUrl = '';

    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function () {
            const serviceTitle = this.getAttribute('data-service-title');
            deleteUrl = this.getAttribute('data-delete-url');

            // Set service title in modal
            document.getElementById('service-title').textContent = serviceTitle;

            // Show modal
            const modalInstance = new bootstrap.Modal(deleteModal);
            modalInstance.show();
        });
    });

    document.getElementById('confirm-delete-btn').addEventListener('click', function(){
        if (deleteUrl){
            fetch(deleteUrl, {
                method: 'DELETE',
                header: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => json.response())
                .then(data => {
                    if(data.success){
                         const modalInstance = bootstrap.Modal.getInstance(deleteModal);
                         modalInstance.hide();

                        const serviceCard = document.querySelector(`[data-delete-url="${deleteUrl}"]`).closest('.col');
                         serviceCard.remove();
                    }
                    else{
                        alert('Error: ' + data.error);
                    }
                })
                .catch(error => console.error('Error: ', error));
        }
    });
});