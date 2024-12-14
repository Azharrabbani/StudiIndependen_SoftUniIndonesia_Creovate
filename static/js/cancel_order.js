function Cancel_order(orderId, orderAt, cancelUrl){
    const now = new Date();
    const orderTime = new Date(orderAt);
    const time_elapsed = Math.abs(now - orderTime);
    const days_elapsed = Math.ceil(time_elapsed / (1000 * 60 * 60 * 24));

    const modalBody = document.getElementById('modalBody');
    const cancelForm = document.getElementById('cancelForm');

    if (days_elapsed > 1){
        modalBody.innerHTML = "<p>This purchase is already pass 24 hours!</p>";
        cancelForm.style.display = 'none';
    }
    else{
        modalBody.innerHTML = "<p>Are you sure you want cancel this purchase?</p>";
        cancelForm.action = cancelUrl;
        cancelForm.style.display = 'block';
    }

    const cancelModal = new bootstrap.Modal(document.getElementById('cancelModal'));
    cancelModal.show();
}