(function($) {
    $(document).ready(function() {
        // Update category dropdown when type changes
        $('#id_type').change(function() {
            var typeId = $(this).val();
            $.ajax({
                url: '/admin/transactions/category/filter_by_type/',
                data: { 'type_id': typeId },
                success: function(data) {
                    $('#id_category').empty();
                    $('#id_category').append('<option value="">---------</option>');
                    $.each(data, function(index, category) {
                        $('#id_category').append('<option value="' + category.id + '">' + category.name + '</option>');
                    });
                    $('#id_category').trigger('change');
                }
            });
        });

        // Update subcategory dropdown when category changes
        $('#id_category').change(function() {
            var categoryId = $(this).val();
            $.ajax({
                url: '/admin/transactions/subcategory/filter_by_category/',
                data: { 'category_id': categoryId },
                success: function(data) {
                    $('#id_subcategory').empty();
                    $('#id_subcategory').append('<option value="">---------</option>');
                    $.each(data, function(index, subcategory) {
                        $('#id_subcategory').append('<option value="' + subcategory.id + '">' + subcategory.name + '</option>');
                    });
                }
            });
        });

        // Trigger change on page load for existing records
        if ($('#id_type').val()) {
            $('#id_type').trigger('change');
        }
    });
})(django.jQuery);