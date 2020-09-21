(function() {
  $("#addFolderButton").on("click", function(event) {
    var button = $(this);
    var endpoint = button.data("endpoint");
    var parent = button.data("parent");
    var modal = $("#createFolderModal");
    var closeButton = modal.find(".close");
    var folder_name = modal.find("#new-folder-name").val();

    var data = {
      is_demo: endpoint !== "folder",
      parent_folder_id: parent,
      folder_name: folder_name
    };

    $.post($URL_ROOT + "folder", data, function(data) {
      var new_folder_id = data["id"] || $("#sidenave a").length + 1;
      var new_folder_url = "/folder/" + data["id"];
      var new_folder_name = "&nbsp;&nbsp;" + data["name"];
      var new_folder =
        '<a href="' +
        new_folder_url +
        '"><i class="fa fa-folder fa_custom"></i>' +
        new_folder_name +
        "</a>";
      $("#sidenav").append(new_folder);
    });

    closeButton.click();
  });
}.call(this));
