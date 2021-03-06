var selected_files = [];

(function() {
  $("#add-folder-button").on("click", function(event) {
    var button = $(this);
    var endpoint = button.data("endpoint");
    var parent = button.data("parent");
    var modal = $("#create-folder-modal");
    var closeButton = modal.find(".close");
    var folder_name = modal.find("#new-folder-name").val();

    var data = {
      is_demo: endpoint !== "folder",
      parent_folder_id: parent,
      folder_name: folder_name
    };

    $.post($URL_ROOT + "folder", data, function(res) {
      var new_folder_id = res["id"] || $("#sidenave a").length + 1;
      var new_folder_url = "/folder/" + res["id"];
      var new_folder_name = "&nbsp;&nbsp;" + res["name"];
      var new_folder =
        '<a href="' +
        new_folder_url +
        '"><i class="fa fa-folder fa_custom"></i>' +
        new_folder_name +
        "</a>";
      $("#sidenav a:first-child").after(new_folder);
    });

    closeButton.click();
  });

  $("#upload-file-button").on("click", function(event) {
    var button = $(this);
    var endpoint = button.data("endpoint");
    var parent = button.data("parent");
    var modal = $("#upload-modal");
    var closeButton = modal.find(".close");
    var file_to_upload = modal.find("#file-to-updload")[0].files[0];

    if (file_to_upload) {
      var data = new FormData();
      data.append("is_demo", endpoint !== "folder");
      data.append("parent_folder_id", parent);
      data.append("file", file_to_upload);

      $.ajax({
        url: $URL_ROOT + "file",
        type: "post",
        data: data,
        contentType: false,
        processData: false,
        success: function(res) {
          var new_file =
            '<tr class="file-row">' +
            '<td class="file-select">' +
            '<label class="checkbox-inline">' +
            '<input type="checkbox" class="checkbox-input" />' +
            "</label>" +
            "</td>" +
            '<td class="file-icon">' +
            '<i class="' +
            res["icon"] +
            '" style="font-size:36px"></i>' +
            "</td>" +
            "<td>" +
            res["name"] +
            "</td>" +
            "</tr>";
          $("#files-table tbody").prepend(new_file);

          $("#upload-modal .modal-content").LoadingOverlay("hide");
          closeButton.click();
        }
      });

      $("#upload-modal .modal-content").LoadingOverlay("show");
    }
  });

  $('input[type="checkbox"]').on("click", function(event) {
    var checkbox = $(this);
    var file = checkbox.data("file");
    if ($(this).is(":checked")) {
      selected_files.push(file);
    } else if ($(this).is(":not(:checked)")) {
      var index = selected_files.indexOf(file);
      if (index > -1) {
        selected_files.splice(index, 1);
      }
    }
  });

  $("#download-button").on("click", function(event) {
    if (selected_files.length > 0) {
      var button = $(this);
      var endpoint = button.data("endpoint");
      var parent = button.data("parent");
      var data = new FormData();
      data.append("is_demo", endpoint !== "folder");
      data.append("parent_folder_id", parent);
      data.append("files", selected_files.join(","));

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          var url = window.URL || window.webkitURL;
          var link = document.createElement("a");
          link.href = url.createObjectURL(this.response);
          link.download = "download.zip";
          link.click();
        }
      };
      xhr.open("POST", $URL_ROOT + "download", true);
      xhr.responseType = "blob";
      xhr.send(data);
    }
  });
}.call(this));
