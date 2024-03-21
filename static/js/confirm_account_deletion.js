function confirmAccountDeletion(){
        var response = confirm("Are you sure you want to delete your account?\nThis cannot be undone...")
        if (response == true){
            return true;
        }else{
            return false;
        }
}