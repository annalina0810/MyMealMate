let currentlyEditedItemId = null;

$(document).ready(function() {
  // Handle adding new items without refreshing the page
  $("#add-item").on("click", function() {
    var name = $("#new-item-name").val();
    var amount = $("#new-item-amount").val();
    var unit = $("#new-item-unit").val();

    if (name || (name && amount) || (name && amount && unit)) {
      console.log("Adding item...")

      $.ajax({
        type: "POST",
        url: "add_item",
        data: {
            'name': name,
            'amount': amount,
            'unit': unit,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function(response) {
            console.log("item added successfully")
            location.reload()
        },
        error: function(error) {
            console.log("Error adding item")
            console.log(error);
        }
      });
    }
  });

  $(".edit-item").on("click", function() {
    console.log("Editing item...")

    var itemId = $(this).data("item-id");
    var listItem = $(this).closest("li");
    if (currentlyEditedItemId) {
        alert('You can only edit one item at a time.');
        return;
    }
    currentlyEditedItemId = itemId;

    // Convert item into form for editing
    var editForm = '<form class="edit-form" data-id="">';
    editForm += '<input type="hidden" id="edit-item-id" name="item-id" value="' + itemId + '">';
    editForm += '<input type="text" id = "edit-name" name="name">';
    editForm += '<input type="number" id = "edit-amount" name="amount">';
    editForm += '<input type="text" id = "edit-unit"  name="unit" ">';
    editForm += '<button class = "button" type="submit">Save</button>';
    editForm += '</form>';

    // Send AJAX request to get item details
    $.ajax({
        type: "GET",
        url: "edit_item",
        data: {
            'item_id': itemId,
        },
        success: function(response) {
            // Populate the form fields with ingredient details
            $("#edit-name").val(response.name);
            $("#edit-amount").val(response.amount);
            $("#edit-unit").val(response.unit);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error:", errorThrown);
        }
    });

    listItem.html(editForm);

   });
    $('#edit-form').click(function() {
        currentlyEditedItemId = null;
    });

  $("#item-list").on("click", ".delete-item", function() {
    var itemId = $(this).data("item-id");
    var listItem = $(this).closest("li");
    $.ajax({
        type: "POST",
        url: "delete_item",
        data: {
            'item_id': itemId,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function(response) {
          console.log("Item deleted successfully");
          // Remove the item from the list on success
          listItem.remove();
      },
        error: function(error) {
          console.log("Error deleting item");
          console.log(error);
        }
    });
  });
});
