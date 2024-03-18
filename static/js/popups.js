function confirmAccountDeletion(){
    if (confirm("Are you sure you want to delete your account?\nThis cannot be undone...")){
        window.location.href = 'delete_account';
   }

}


function clearAll(){
    if (confirm("Are you sure you want to clear all the items from your shopping list?\nThis cannot be undone...")){
        window.location.href = 'clear_all';
    }
}

