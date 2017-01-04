Faceted.Options.FADE_SPEED=0;
Faceted.Options.SHOW_SPINNER=false;

// Function that allows to generate a document aware of table listing documents in a faceted navigation.
function generatePodDocument(template_uid, output_format, tag) {
    theForm = $(tag).parents('form')[0];
    theForm.template_uid.value = template_uid;
    theForm.output_format.value = output_format;
    // manage the facetedquery
    theForm.facetedQuery.value = JSON.stringify(Faceted.Query);
    var hasCheckBoxes = $('input[name="select_item"]');
    // if there are checkboxes on a faceted, get uids
    if (hasCheckBoxes.length != 0) {
        // if not on a faceted, do not manage uids, we have no table
        if ($('div#faceted-results').length) {
            var uids = selectedCheckBoxes('select_item');
            if (!uids.length) {
                alert(no_selected_items);
                return
            }
            else {
                // if we unselected some checkboxes, we pass uids
                // else, we pass nothing, it is as if we did selected everything
                if ($('input[name="select_item"]').length === uids.length) {
                    uids = [];
                }
                theForm.uids.value = uids;
            }
        }
    }
    theForm.submit();
}

$(document).ready(function () {
  var url = $('base').attr('href') + '/@@json_collections_count';
  if ($('.faceted-tagscloud-collection-widget').length > 0) {
    $(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function() {
        $.get(url, function (response) {
            var info = JSON.parse(response);
            var criterionId = info.criterionId;
            var countByCollection = info.countByCollection;
            countByCollection.forEach(function (item) {
              $('li#' + criterionId + item.uid + ' .term-count').html(item.count);
            })
        })
    });
  }
})
