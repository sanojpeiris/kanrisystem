function1 () 
    var r = confirm("ARE YOU SURE!");
    if (r == true) {location.href = "/deleteTask_id/{{ task_item.id }}";} else {return false;};
    