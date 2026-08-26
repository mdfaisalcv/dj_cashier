var base_url=location.protocol + "//" + location.hostname + (location.port && ":" + location.port) + "/[[=request.app_name]]/";

    $(document).ready(function () {
        $(".geo_target_others").hide();
        $("#new_client_div").hide();
        $("#client_link").hide();//Client file or client_link upload
        $("#creative_link").hide();//Creative file or creative_link upload
        $("#invoice_link").hide();//Invoice file or invoice_link upload
        $("#invoiceFile").hide();
        $("#landing_file").hide();
        $(".selectChange").each(function () {
            $(this).select2({
                placeholder: "--Select--",
                allowClear: true,
            });
        });
        
        

        $('#segment').on('change', function () {
            segmentChange("#tbody tr")
        });
       
        
        //  Bind recalculation on inputs
        $("#tbody").on('keyup blur', 'input[name="quantity"], input[name="cpm"], input[name="cpm_discount_per"]', function () {
            recalculateTotals();
        });

        //  Also bind recalculation when special discount changes
        $("#special_discount").on('keyup blur change', function () {
            recalculateTotals();
        });


        //=======================client approval file upload
        let formDataListClient = [];
        $('#clientUploadFileBtn').on('click', function (e) {
            e.preventDefault();

            let client_file_type = $('#client_file_type').val();
            let client_link = $('#client_link').val().trim();
            let fileInput = $('#client_approval_file')[0];

            if (client_file_type === 'File') {
                if (!fileInput || fileInput.files.length === 0) {
                    Toast.fire({ icon: "warning", title: "Please select at least one file" });
                    return;
                }

                let file = fileInput.files[0];

                // File size validation (limit: 50MB)
                if (file.size > 50 * 1024 * 1024) {
                    Toast.fire({
                        icon: "error",
                        title: "File size must be 50MB or less"
                    });
                    $('#client_approval_file').val('');
                    return;
                }

                for (let i = 0; i < fileInput.files.length; i++) {
                    let file = fileInput.files[i];

                    formDataListClient.push({
                        client_file_type: 'File',
                        client_link: '',
                        client_approval_file_name: file.name,
                        file_object: file // keep in memory only, not in hidden input
                    });
                }

                toggleClientUploadSpinner(true);

                $('#client_approval_file').val('');
                $('#client_link').val('');

            } else if (client_file_type === 'Link') {
                if (!client_link) {
                    Toast.fire({ icon: "warning", text: "Please provide a valid link" });
                    return;
                }

                formDataListClient.push({
                    client_file_type: 'Link',
                    client_link: client_link,
                    client_approval_file_name: ''
                });

                toggleClientUploadSpinner(true);

                $('#client_approval_file').val('');
                $('#client_link').val('');
            } else {
                alert("Invalid file type selected.");
                return;
            }

            // Set only metadata (exclude file objects)
            const metadataListClient = formDataListClient.map(item => ({
                client_file_type: item.client_file_type,
                client_link: item.client_link,
                client_approval_file_name: item.client_approval_file_name
            }));

            $('#clientUploadFileLink').val(JSON.stringify(metadataListClient));

            clientUpdateTable();

        });
        
        $("#client_file_type").on( "change", function() {
            var fileType = $('#client_file_type').val();
            if (fileType=='File'){
                $("#client_link").hide();
                $("#client_approval_file").show();
            }else{
                $("#client_link").show();
                $("#client_approval_file").hide();
            }            
        })

        function clientUpdateTable() {
            let tableBody = $('#client_approve_table tbody');
            tableBody.empty();
            toggleClientUploadSpinner(false);
            formDataListClient.forEach((item, index) => {
                let displayName = item.client_file_type === 'File' 
                    ? item.client_approval_file_name 
                    : `<a href="${item.client_link}" target="_blank">${item.client_link}</a>`;

                let downloadIcon = item.client_file_type === 'File' 
                    ? `<i class="fa-solid fa-arrow-down text-muted"></i>` // Placeholder; actual link needs backend
                    : '';

                let newRow = `
                    <tr>
                        <td width="90%">${displayName}</td>
                        <!--<td class="text-center" width="10%">${downloadIcon}</td>-->
                    </tr>
                `;

                tableBody.append(newRow);
            });
        }


        //=======================creative file upload
        let formDataListCreative = [];
        $('#creativeUploadFileBtn').on('click', function (e) {
            e.preventDefault();

            let creative_file_type = $('#creative_file_type').val();
            let creative_link = $('#creative_link').val().trim();
            let fileInput = $('#creative_file')[0];

            if (creative_file_type === 'File') {
                if (!fileInput || fileInput.files.length === 0) {
                    Toast.fire({ icon: "warning", title: "Please select at least one file" });
                    return;
                }

                let file = fileInput.files[0];

                // File size validation (limit: 50MB)
                if (file.size > 50 * 1024 * 1024) {
                    Toast.fire({
                        icon: "error",
                        title: "File size must be 50MB or less"
                    });
                    $('#creative_file').val('');
                    return;
                }


                for (let i = 0; i < fileInput.files.length; i++) {
                    let file = fileInput.files[i];

                    formDataListCreative.push({
                        creative_file_type: 'File',
                        creative_link: '',
                        creative_file_name: file.name,
                        file_object: file // file stored in memory, not in hidden input
                    });
                }

                toggleCreativeUploadSpinner(true);

                $('#creative_file').val('');
                $('#creative_link').val('');

            } else if (creative_file_type === 'Link') {
                if (!creative_link) {
                    Toast.fire({ icon: "warning", text: "Please provide a valid link" });
                    return;
                }

                formDataListCreative.push({
                    creative_file_type: 'Link',
                    creative_link: creative_link,
                    creative_file_name: ''
                });

                toggleCreativeUploadSpinner(true);

                $('#creative_file').val('');
                $('#creative_link').val('');
            } else {
                alert("Invalid file type selected.");
                return;
            }

            // Metadata only (no actual files)
            const metadataListCreative = formDataListCreative.map(item => ({
                creative_file_type: item.creative_file_type,
                creative_link: item.creative_link,
                creative_file_name: item.creative_file_name
            }));

            $('#creativeUploadFileLink').val(JSON.stringify(metadataListCreative));

            creativeUpdateTable();
        });
        
        $("#creative_file_type").on( "change", function() {
            var fileType = $('#creative_file_type').val();
            if (fileType=='File'){
                $("#creative_link").hide();
                $("#creative_file").show();
            }else{
                $("#creative_link").show();
                $("#creative_file").hide();
            }            
        })

        function creativeUpdateTable() {
            let tableBody = $('#creative_table tbody');
            tableBody.empty();
            toggleCreativeUploadSpinner(false);

            formDataListCreative.forEach((item, index) => {
                let displayName = item.creative_file_type === 'File' 
                    ? item.creative_file_name 
                    : `<a href="${item.creative_link}" target="_blank">${item.creative_link}</a>`;

                let downloadIcon = item.creative_file_type === 'File' 
                    ? `<i class="fa-solid fa-arrow-down text-muted"></i>` // Placeholder; actual link needs backend
                    : '';

                let newRow = `
                    <tr>
                        <td width="90%">${displayName}</td>
                        <!--<td class="text-center" width="10%">${downloadIcon}</td>-->
                    </tr>
                `;

                tableBody.append(newRow);
            });
        }


        //=======================Invoice file upload
        let formDataListInvoice = [];
        $('#invoiceUploadFileBtn').on('click', function (e) {
            e.preventDefault();

            let invoice_file_type = $('#invoice_file_type').val();
            let invoice_link = $('#invoice_link').val().trim();
            let fileInput = $('#invoice_file')[0];

            if (invoice_file_type === 'File') {
                if (!fileInput || fileInput.files.length === 0) {
                    Toast.fire({ icon: "warning", text: "Please select at least one file" });
                    return;
                }

                let file = fileInput.files[0];

                // File size validation (limit: 50MB)
                if (file.size > 50 * 1024 * 1024) {
                    Toast.fire({
                        icon: "error",
                        title: "File size must be 50MB or less"
                    });
                    $('#invoice_file').val('');
                    return;
                }

                for (let i = 0; i < fileInput.files.length; i++) {
                    let file = fileInput.files[i];

                    formDataListInvoice.push({
                        invoice_file_type: 'File',
                        invoice_link: '',
                        invoice_file_name: file.name,
                        file_object: file // in-memory only
                    });
                }

                toggleInvoiceUploadSpinner(true);

                $('#invoice_file').val('');
                $('#invoice_link').val('');

            } else if (invoice_file_type === 'Link') {
                if (!invoice_link) {
                    Toast.fire({ icon: "warning", text: "Please provide a valid link" });
                    return;
                }

                formDataListInvoice.push({
                    invoice_file_type: 'Link',
                    invoice_link: invoice_link,
                    invoice_file_name: ''
                });

                toggleInvoiceUploadSpinner(true);

                $('#invoice_file').val('');
                $('#invoice_link').val('');
            } else {
                alert("Invalid file type selected.");
                return;
            }

            // Store metadata only (not actual files)
            const metadataListInvoice = formDataListInvoice.map(item => ({
                invoice_file_type: item.invoice_file_type,
                invoice_link: item.invoice_link,
                invoice_file_name: item.invoice_file_name
            }));

            $('#invoiceUploadFileLink').val(JSON.stringify(metadataListInvoice));

            invoiceUpdateTable();
        });
        
        $("#invoice_file_type").on( "change", function() {
            var fileType = $('#invoice_file_type').val();
            if (fileType=='File'){
                $("#invoice_link").hide();
                $("#invoice_file").show();
            }else{
                $("#invoice_link").show();
                $("#invoice_file").hide();
            }            
        })
        
        function invoiceUpdateTable() {
            let tableBody = $('#invoice_table tbody');
            tableBody.empty();
            toggleInvoiceUploadSpinner(false);

            formDataListInvoice.forEach((item, index) => {
                let displayName = item.invoice_file_type === 'File' 
                    ? item.invoice_file_name 
                    : `<a href="${item.invoice_link}" target="_blank">${item.invoice_link}</a>`;

                let downloadIcon = item.invoice_file_type === 'File' 
                    ? `<i class="fa-solid fa-arrow-down text-muted"></i>` // Placeholder; actual link needs backend
                    : '';

                let newRow = `
                    <tr>
                        <td width="90%">${displayName}</td>
                        <!--<td class="text-center" width="10%">${downloadIcon}</td>-->
                    </tr>
                `;

                tableBody.append(newRow);
            });
        }
        //=======================Landing Link upload
        let formDataListLanding = [];
        $('#landingUploadFileBtn').on('click', function (e) {
            e.preventDefault();

            let landing_file_type = $('#landing_file_type').val();
            let landing_link = $('#landing_link').val().trim();
            let fileInput = $('#landing_file')[0];

            if (landing_file_type === 'File') {
                if (!fileInput || fileInput.files.length === 0) {
                    Toast.fire({ icon: "warning", title: "Please select at least one file" });
                    return;
                }

                let file = fileInput.files[0];

                // File size validation (limit: 50MB)
                if (file.size > 50 * 1024 * 1024) {
                    Toast.fire({
                        icon: "error",
                        title: "File size must be 50MB or less"
                    });
                    $('#landing_file').val('');
                    return;
                }

                for (let i = 0; i < fileInput.files.length; i++) {
                    let file = fileInput.files[i];

                    formDataListLanding.push({
                        landing_file_type: 'File',
                        landing_link: '',
                        landing_file_name: file.name,
                        file_object: file // in-memory only
                    });
                }

                toggleLandingUploadSpinner(true);
                $('#landing_file').val('');
                $('#landing_link').val('');

            } else if (landing_file_type === 'Link') {
                if (!landing_link) {
                    Toast.fire({ icon: "warning", text: "Please provide a valid link" });
                    return;
                }

                formDataListLanding.push({
                    landing_file_type: 'Link',
                    landing_link: landing_link,
                    landing_file_name: ''
                });

                toggleLandingUploadSpinner(true);

                $('#landing_file').val('');
                $('#landing_link').val('');
            } else {
                alert("Invalid file type selected.");
                return;
            }

            // Store only metadata for backend
            const metadataListLanding = formDataListLanding.map(item => ({
                landing_file_type: item.landing_file_type,
                landing_link: item.landing_link,
                landing_file_name: item.landing_file_name
            }));

            $('#landingUploadFileLink').val(JSON.stringify(metadataListLanding));

            landingUpdateTable();
        });
        
        $("#landing_file_type").on( "change", function() {
            var fileType = $('#landing_file_type').val();
            if (fileType=='File'){
                $("#landing_link").hide();
                $("#landing_file").show();
            }else{
                $("#landing_link").show();
                $("#landing_file").hide();
            }            
        })
        
        function landingUpdateTable() {
            let tableBody = $('#landing_table tbody');
            tableBody.empty();

            toggleLandingUploadSpinner(false);

            formDataListLanding.forEach((item, index) => {
                let displayName = item.landing_file_type === 'File' 
                    ? item.landing_file_name 
                    : `<a href="${item.landing_link}" target="_blank">${item.landing_link}</a>`;

                let downloadIcon = item.landing_file_type === 'File' 
                    ? `<i class="fa-solid fa-arrow-down text-muted"></i>` // Placeholder; actual link needs backend
                    : '';

                let newRow = `
                    <tr>
                        <td width="90%">${displayName}</td>
                        <!--<td class="text-center" width="10%">${downloadIcon}</td>-->
                    </tr>
                `;

                tableBody.append(newRow);
            });
        }


        $("form").submit(function(event) {
            event.preventDefault(); // Prevent default form submission

            var form = $(this); // Store form reference
            var submitButton = form.find(":submit"); // Find the submit button in the form
            var spinner = submitButton.find("#spinner"); // Find the spinner inside the button

            // Disable the button and show the spinner
            submitButton.prop("disabled", true);
            spinner.show();

            var formData = new FormData(this); // Collect all form data
            //===========client file
            const metadataListClient = formDataListClient;
            metadataListClient.forEach((item, i) => {
                formData.append(`data[${i}][client_file_type]`, item.client_file_type);
                formData.append(`data[${i}][client_link]`, item.client_link);
                formData.append(`data[${i}][client_approval_file_name]`, item.client_approval_file_name);
                if (item.client_file_type === 'File') {
                    formData.append(`data[${i}][client_approval_file]`, item.file_object);
                }
            });
            //===========Creative file
            const metadataListCreative = formDataListCreative;
            metadataListCreative.forEach((item, i) => {
                formData.append(`data[${i}][creative_file_type]`, item.creative_file_type);
                formData.append(`data[${i}][creative_link]`, item.creative_link);
                formData.append(`data[${i}][creative_file_name]`, item.creative_file_name);
                if (item.creative_file_type === 'File') {
                    formData.append(`data[${i}][creative_file]`, item.file_object);
                }
            });
            //===========Invoice file
            const metadataListInvoice = formDataListInvoice;
            metadataListInvoice.forEach((item, i) => {
                formData.append(`data[${i}][invoice_file_type]`, item.invoice_file_type);
                formData.append(`data[${i}][invoice_link]`, item.invoice_link);
                formData.append(`data[${i}][invoice_file_name]`, item.invoice_file_name);
                if (item.invoice_file_type === 'File') {
                    formData.append(`data[${i}][invoice_file]`, item.file_object);
                }
            });

            //===========Landing Link
            const metadataListLanding = formDataListLanding;
            metadataListLanding.forEach((item, i) => {
                formData.append(`data[${i}][landing_file_type]`, item.landing_file_type);
                formData.append(`data[${i}][landing_link]`, item.landing_link);
                formData.append(`data[${i}][landing_file_name]`, item.landing_file_name);
                if (item.landing_file_type === 'File') {
                    formData.append(`data[${i}][landing_file]`, item.file_object);
                }
            });

            $.ajax({
                url: this.action, // URL for the form submission
                type: 'POST', // Form method (POST)
                data: formData, // Form data
                processData: false, // Required for sending FormData
                contentType: false, // Set content type to false for FormData
                success: function(response) {
                    console.log(response)
                    try {
                        if (response && response.message && response.status) {
                            const fullMessage = response.message.replaceAll('rdrdrd', '\n'); // Replace all 'rdrdrd' with '\n'
                            
                            Toast.fire({
                                icon: response.status, // Assuming 'success', 'error', etc.
                                title: fullMessage, // Display concatenated message
                            });
                            if (response.status === 'success') {
                                setTimeout(function() {
                                    window.location.href = base_url+"io/index";
                                }, 3000); // Redirects after 3 seconds
                            } else {
                                submitButton.prop("disabled", false); // Re-enable the button if there is an error
                                spinner.hide(); // Hide the spinner
                            }
                        } else {
                            console.error("Unexpected response format:", response);
                            alert("Unexpected response from server.");
                            submitButton.prop("disabled", false); // Re-enable the button
                            spinner.hide(); // Hide the spinner
                        }
                    } catch (error) {
                        console.error("Error processing response:", error);
                        alert("Error processing response.");
                        submitButton.prop("disabled", false); // Re-enable the button
                        spinner.hide(); // Hide the spinner
                    }
                },
                error: function(xhr, status, error) {
                    alert('Error submitting form: ' + error);
                    console.log(xhr.responseText); // Optional: for debugging
                    submitButton.prop("disabled", false); // Re-enable the button in case of error
                    spinner.hide(); // Hide the spinner
                }
            });
        });

        
        flatpickr(".date-picker[name='campaign_end']", {
            dateFormat: "F j, Y", // This gives format like "July 23, 2025"
            onChange: function (selectedDates, dateStr, instance) {
                if (dateStr) {
                    console.log("Selected Date:", dateStr);
                    // Enable and trigger click on the Add button
                    $('.addBtn').prop('disabled', false).click();
                } else {
                    // Disable the Add button if the date is cleared
                    $('.addBtn').prop('disabled', true);
                }
            }
        });



    });

    function toggleClientUploadSpinner(isLoading) {
        let $btn = $('#clientUploadFileBtn');
        let $btnText = $btn.find('.btn-text');
        
        if (isLoading) {
            $btn.prop('disabled', true);
            $btnText.html('<i class="fa fa-spinner fa-spin"></i>');
        } else {
            $btn.prop('disabled', false);
            $btnText.html('<i class="fa-solid fa-cloud-arrow-up"></i>');
        }
    }
    
    function toggleCreativeUploadSpinner(isLoading) {
        let $btn = $('#creativeUploadFileBtn');
        let $btnText = $btn.find('.btn-text');
        
        if (isLoading) {
            $btn.prop('disabled', true);
            $btnText.html('<i class="fa fa-spinner fa-spin"></i>');
        } else {
            $btn.prop('disabled', false);
            $btnText.html('<i class="fa-solid fa-cloud-arrow-up"></i>');
        }
    }
    
    function toggleLandingUploadSpinner(isLoading) {
        let $btn = $('#landingUploadFileBtn');
        let $btnText = $btn.find('.btn-text');
        
        if (isLoading) {
            $btn.prop('disabled', true);
            $btnText.html('<i class="fa fa-spinner fa-spin"></i>');
        } else {
            $btn.prop('disabled', false);
            $btnText.html('<i class="fa-solid fa-cloud-arrow-up"></i>');
        }
    }
    
    function toggleInvoiceUploadSpinner(isLoading) {
        let $btn = $('#invoiceUploadFileBtn');
        let $btnText = $btn.find('.btn-text');
        
        if (isLoading) {
            $btn.prop('disabled', true);
            $btnText.html('<i class="fa fa-spinner fa-spin"></i>');
        } else {
            $btn.prop('disabled', false);
            $btnText.html('<i class="fa-solid fa-cloud-arrow-up"></i>');
        }
    }
    
    function recalculateTotals() {
        var subtotal = 0;
        var subtotal_vat = 0;
        var net_total = 0;
        var discountTotal = 0;
        var vatableAmountTotal = 0;
        var net_discount = 0;

        //  Parse and round special discount
        var special_discount = Math.round(parseFloat($("#special_discount").val()) || 0);
        var vatPercent = Math.round(parseFloat($("#vatPercent").val()) || 0);

        $("#tbody tr").each(function () {
            var $row = $(this);
            var calculation = $row.find('input[name="calculation"]').val() || 0;
            var qty = parseFloat($row.find('input[name="quantity"]').val()) || 0;
            var cpm = parseFloat($row.find('input[name="cpm"]').val()) || 0;
            var cpm_desc_per = parseFloat($row.find('input[name="cpm_discount_per"]').val()) || 0;
            
            let amount_total = 0;
            if (calculation === 'Impression') {
                amount_total = (qty * cpm) / 1000;
            } else {
                amount_total = qty * cpm;
            }

            $row.find('input[name="cpm_amount"]').val(amount_total.toFixed(2));
            subtotal += amount_total;

            if (!isNaN(cpm_desc_per)) {
                if (cpm_desc_per > 20) {
                    Toast.fire({
                        text: "Discount cannot be greater than 20%!",
                        icon: "warning"
                    });
                    $row.find('input[name="cpm_discount_per"]').val(0);
                    $row.find('input[name="cpm_discount_amount"]').val(0);
                    $row.find("#cpm_discount_gross_amount").val(0);
                } else {
                    // let discount_amount_total = Math.round((amount_total * cpm_desc_per) / 100);
                    // $row.find('input[name="cpm_discount_amount"]').val(discount_amount_total);
                    // discountTotal += discount_amount_total;

                    // let discount_gross_amount_total = Math.round(amount_total - discount_amount_total);
                    // $row.find("#cpm_discount_gross_amount").val(discount_gross_amount_total);

                    discount_amount_total = (amount_total * cpm_desc_per) / 100;
                    $row.find('input[name="cpm_discount_amount"]').val(discount_amount_total.toFixed(2));
                    discountTotal += discount_amount_total;
                    discount_gross_amount_total = amount_total.toFixed(2) - discount_amount_total.toFixed(2)
                    $row.find("#cpm_discount_gross_amount").val(discount_gross_amount_total.toFixed(2));

                }
            }
        });

        net_discount = discountTotal + special_discount;
        vatableAmountTotal = Math.round(subtotal - net_discount);
        subtotal_vat = Math.round(vatableAmountTotal * vatPercent / 100);
        net_total = (subtotal - net_discount) + subtotal_vat;

        $("#subTotal").html(Math.round(subtotal).toLocaleString());
        $("#discount").html(Math.round(discountTotal).toLocaleString());
        $("#vatable_amount").html(vatableAmountTotal.toLocaleString());
        $("#vat").html(subtotal_vat.toLocaleString());
        $("#net_total").html(Math.round(net_total).toLocaleString());

        $("#sub_total").val(Math.round(subtotal));
        $("#discount_total").val(Math.round(discountTotal));
        $("#total_vatable_amount").val(vatableAmountTotal);
        $("#vat_amount").val(subtotal_vat);
        $("#net_total_amount").val(Math.round(net_total));
    }


    function sweetAlert() {
        Toast.fire({
            // title: "Warning",
            text: "Required all",
            icon: "warning"
        });
    }
   
    var rowIndex = 1;
    $(".addBtn").click(function () {  
        let allowAppend = true;
        
        if (rowIndex > 1) {
            var client = $('#client').val();
            var segment = $('#segment').val();
            var proposal_date = $('#proposal_date').val();

            var lastRow = $("#tbody tr:last-child");
            var brand = lastRow.find('.brand').val();
            var campaign_duration = lastRow.find('.campain_duration').val();
            var c_start_date = lastRow.find('.c_start_date').val();
            var c_end_date = lastRow.find('.c_end_date').val();
            var site = lastRow.find('.site').val();
            var section = lastRow.find('.section').val();
            var ad_type = lastRow.find('.ad_type').val();
            var singleRow = lastRow.find('.singleRow').val();
            var geo_target = lastRow.find('.geo_target').val();
            var publication = lastRow.find('.publication').val();
            var cpm = parseFloat(lastRow.find('.cpm').val());
            var qty = lastRow.find('.qty').val();

            if (client === '' || segment === '' || proposal_date === '' || brand === '' || campaign_duration === '' || site === '' || section === '' || ad_type === '' || singleRow === '' || geo_target === '' || publication.length === 0 || isNaN(cpm) || cpm === 0 || qty === '') {
                sweetAlert();
                allowAppend = false;
            }
        }

        if (!allowAppend) return; // stop here if validation failed

        // Append row here
        var campaign_start = $('#campaign_start').val();
        var campaign_end = $('#campaign_end').val();
        console.log(campaign_start)

        $("#tbody").append(`
            <tr class="rowClass"> 
                <td class="row-index text-center">  
                    <div class="col-md-12" style="width:150px">
                        <div class="" id="brand">
                            <select class="select_custom form-control form-select-sm selectChange brand" name="brand" >
                                <option value="">--Select--</option>
                            
                            </select>
                        </div>                        
                    </div>                                   
                </td> 
                <td class="row-index text-center">                    
                    <div class="col-md-12" style="width:120px">
                        <div class="">
                            <input type="text" class="form-control form-control-sm campain_duration" id="campain_duration" name="campain_duration" maxlength="50">  
                        </div>
                    </div>                   
                </td> 
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:120px">
                        <div class="flatpickr-wrapper">
                            <input type="text" class="form-control form-control-sm date-picker c_start_date" name="c_start_date" placeholder="Start Date" value="${campaign_start}">
                            <i class="fa fa-calendar calendar-icon text-secondary calendar-toggle"></i>                            
                        </div>
                    </div>
                </td>
                
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:120px">
                        <div class="flatpickr-wrapper">
                            <input type="text" class="form-control form-control-sm date-picker c_end_date" name="c_end_date" placeholder="End Date" value="${campaign_end}">
                            <i class="fa fa-calendar calendar-icon text-secondary calendar-toggle"></i>                            
                        </div>
                    </div>
                </td>
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:150px">
                        <div class="">
                            <select class="select_custom form-control form-select-sm selectChange site"
                                name="site">
                                <option value="">--Select--</option>
                                [[for row in siteRec:]]
                                <option value="[[=row.site]]">[[=row.site]]</option>
                                [[pass]]
                            </select>
                        </div>
                    </div>
                </td>
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:150px">
                        <div class="">
                            <select class="select_custom form-control form-select-sm selectChange section"
                                name="section">
                                <option value="">--Select--</option>
                                
                            </select>
                        </div>
                    </div>
                </td> 
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:120px">
                        <div class="">
                            <select class="select_custom form-control form-select-sm selectChange ad_type" name="ad_type"  >
                                <option value="">--Select--</option>
                            </select>
                        </div>                        
                    </div>
                </td> 
                <td class="row-index text-center">
                    <table class="table table-bordered radius mb-0 ">
                        <tbody class="">
                            <tr style="background-color: #ccc9fa;">
                                <td>
                                    <div class="col-md-12" style="width:120px">
                                        <div class="">
                                            <input type="hidden" class="singleRow" name="adPlDevAdsize_${rowIndex}">
                                            <select
                                                class="select_custom form-control form-select-sm selectChange selectmulti site_section"
                                                name="site_section">
                                                <option value="">--Select--</option>

                                            </select>

                                        </div>
                                    </div>
                                </td>
                                <td class="row-index text-center">
                                    <div class="col-md-12" style="width:120px">
                                        <div class="">
                                            <select class="select_custom form-control form-select-sm selectChange device"
                                                name="device">
                                                <option value="">--Select--</option>
                                                
                                            </select>
                                        </div>
                                    </div>
                                </td>
                                <td class="row-index text-center">
                                    <div class="col-md-12" style="width:120px">
                                        <div class="" id="ad_size">
                                            <select class="select_custom form-control form-select-sm selectChange adsize"
                                                name="adsize">
                                                <option value="">--Select--</option>
                                                
                                            </select>
                                        </div>
                                    </div>
                                </td>
                                <td class="addQue">
                                    <a href="#"><i class="fa-solid fa-circle-plus"></i></a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <table width="400" class="table table-bordered radius mb-0 ">
                        <tbody class="tableClass">
                        </tbody>
                    </table>        
                </td>            
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:120px">
                        <div class="" id="geo_target">
                            <select class="select_custom form-control form-select-sm selectChange geo_target" name="geo_target" >
                                <option value="">--Select--</option>
                            </select>

                            <input type="text" class="form-control form-control-sm geo_target_others mt-1" id="geo_target_others" maxlength="50" name="geo_target_others">
                        </div>                        
                    </div>
                </td>
                
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:120px">
                        <div class="" id="publication">
                            <select class="select_custom form-control form-select-sm selectChange publication" name="publication_${rowIndex}" multiple>
                                <option value="">--Select--</option>                            
                                
                            </select>
                        </div>                        
                    </div>
                </td>
                <td class="row-index text-center"> 
                    <div class="col-md-12" style="width:80px">
                        <div class="">
                            <input type="hidden" class="form-control form-control-sm calculation" id="calculation" name="calculation">
                            <input type="text" class="form-control form-control-sm cpm" id="cpm" name="cpm" min="0" value=0 style="text-align:right">
                        </div>
                    </div>                     
                </td> 
                <td class="row-index text-center"> 
                    <div class="col-md-12" style="width:80px">
                        <div class="">
                            <input type="text" class="form-control form-control-sm qty" id="quantity" name="quantity" min="0" value=0 style="text-align:right"> 
                        </div>
                    </div>                     
                </td>                               
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:80px">
                        <div class="">
                            <input type="text" class="form-control form-control-sm" id="cpm_amount" name="cpm_amount" min="0" value=0 readonly style="text-align:right">
                        </div>
                    </div>
                </td>
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:50px">
                        <div class="">
                            <input type="text" class="cpm_disc" id="cpm_discount_per" name="cpm_discount_per" min="0" value=0 style="text-align:right">
                        </div>
                    </div>
                </td> 
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:80px">
                        <div class="">
                            <input type="text" class="form-control form-control-sm" id="cpm_discount_amount" name="cpm_discount_amount" value=0 readonly style="text-align:right">
                        </div>
                    </div>
                </td>   
                <td class="row-index text-center">
                    <div class="col-md-12" style="width:80px">
                        <div class="">
                            <input type="text" class="form-control form-control-sm" id="cpm_discount_gross_amount" name="cpm_discount_gross_amount" value=0 readonly style="text-align:right">
                        </div>
                    </div>
                </td>   
                <td class="text-center okr_list_delete">                 
                    <a class="text-danger remove" href="#"><i class="fas fa-trash"></i></a>
                    
                </td> 
            </tr>
        ` );

        $("#tbody tr:last-child .date-picker").flatpickr({
            dateFormat: "F j, Y"
        });

        
        $(".selectChange").each(function () {
            $(this).select2({
                // dropdownParent: $("#custom_form"),
                placeholder: "--Select--",
                allowClear: true,
            });
        });
        
        segmentChange("#tbody tr:last-child")
        
        rowIndex++;
    });

    //=========row remove
    $("#tbody").on("click", ".okr_list_delete", function () {
        var $currentElement = $(this);
        $currentElement.closest('tr').find('input[name="quantity"]').val('').blur();
        $(this).parent('tr').remove();
    });

    $(document).on("change", "#client", function () {
        //var client = $('#client').val();
        var client = $(this).val();
        if (client=='0'){
            $("#new_client_div").show();
        }else{
            $("#new_client_div").hide();
        }
        $.ajax({
            url: '[[=URL("default","get_client_info")]]',
            method: 'GET',
            data: { q: client },
            dataType: 'json',
            success: function (data) {    
                //console.log(data['results']['client_info'][0]['vat'])            
                var vat = (data['results']['client_info'] && data['results']['client_info'][0] && data['results']['client_info'][0]['vat']) ? data['results']['client_info'][0]['vat'] : 0;
                $("#vatShow").html(vat + '%');
                $("#vatPercent").val(vat);
                
                //console.log(data['results']['client_info']);
                $("#bill_to_customer").val(data['results']['client_info'][0]['name']);
                $("#bill_to_address1").val(data['results']['client_info'][0]['address']);
                $("#bill_to_address2").val(data['results']['client_info'][0]['second_address']);
                $("#bill_to_city").val(data['results']['client_info'][0]['city']);
                $("#bill_to_contact_person").val(data['results']['client_info'][0]['contact_person']);
                $("#bill_to_email").val(data['results']['client_info'][0]['email']);
                $("#bill_to_phone").val(data['results']['client_info'][0]['phone_number']);
                $("#po_ro_number").val(data['results']['client_info'][0]['accpac_code']);
                $("#credit_limit").val(data['results']['client_info'][0]['credit_limit']);
                $("#current_due").val(data['results']['client_info'][0]['current_due']);

                // console.log(data['results']['agency_info']);            
                // $("#agency_contact").val(data['results']['agency_info'][0]['agency_name']);
                // $("#phone_no").val(data['results']['agency_info'][0]['contact_no']);
                // $("#agency_email").val(data['results']['agency_info'][0]['agency_email']);

                if (data['results']['agency_info'] && data['results']['agency_info'].length > 0) {
                    $("#agency_contact").val(data['results']['agency_info'][0]['agency_name']);
                    $("#phone_no").val(data['results']['agency_info'][0]['contact_no']);
                    $("#agency_email").val(data['results']['agency_info'][0]['agency_email']);
                } else {
                    // Optional: clear previous values or show placeholders
                    $("#agency_contact").val('');
                    $("#phone_no").val('');
                    $("#agency_email").val('');
                }


                //console.log(data['results']['advertiser']);  
                var $select = $('#advertiser'); // directly get by ID

                // Clear the existing options
                $select.empty();
                // Add the default placeholder option
                $select.append('<option value="">--Select--</option>');

                // Append new options
                $.each(data['results']['advertiser'], function (key, value) {
                    $select.append(`<option value="${value.id}">${value.advertiser_name}</option>`);
                });

                // Destroy Select2 instance if already initialized
                if ($select.hasClass("select2-hidden-accessible")) {
                    $select.select2('destroy');
                }

                // Reinitialize Select2
                $select.select2({
                    placeholder: "--Select--",
                    allowClear: true,
                    width: '100%' // ensures proper width
                });



            }
        });

       // $('#segment').val('');
        // $(".selectChange").each(function () {
        //     $(this).select2({
        //         placeholder: "--Select--",
        //         allowClear: true,
        //     });
        // });


        //$('#segment').change();
        // }
    });

    $(document).on("change", ".site", function () {
        var site = $(this).val();
        var $select = $(this).closest('tr').find('.section')
        $.ajax({
            url: '[[=URL("default","get_section")]]',
            method: 'GET',
            data: { site: site },
            dataType: 'json',
            success: function (data) {
                $select.empty();
                $select.append('<option value="">--Select--</option>');

                // Append new options
                $.each(data['results'], function (key, value) {
                    $select.append(`<option value="${value.section}">${value.section}</option>`);
                });

                // Reinitialize select2 with new options
                $select.select2({
                    placeholder: "--Select--",
                    allowClear: true,
                });
            }
        });
    })

    $(document).on("change", ".ad_type", function () {
        var segment = $('#segment').val();
        var ad_type = $(this).val();
        var $select = $(this).closest('tr').find('.site_section');
        var $currentElement = $(this);
        if (segment == '') {
            Toast.fire({
                // title: "Warning",
                text: "Required segment",
                icon: "warning"
            });
        } else if (ad_type == '') {
            Toast.fire({
                // title: "Warning",
                text: "Required ad type",
                icon: "warning"
            });
        } else {
            $.ajax({
                url: '[[=URL("default","get_ad_placement")]]',
                method: 'GET',
                data: { segment: segment, ad_type: ad_type },
                dataType: 'json',
                success: function (data) {
                    var results = data['results'];
                    //console.log(results)
                    // Ensure results exist
                    var rate = 0;
                    var impression = '';
                    if (results.length > 0) {
                        // Extract first row's ad placement and rate
                        var adPlacementList = results.map(function (item) { return item.ad_placement; });
                        rate = results[0].rate;
                        //console.log(rate)
                        impression = results[0].impression;
                        // Set rate value in the input field
                        if (rate === 0) {
                            $currentElement.closest('tr').find('input[name="cpm"]').val(rate).attr("readonly", false);
                        } else {
                            $currentElement.closest('tr').find('input[name="cpm"]').val(rate).attr("readonly", true);
                        }
                        // Set impression value in the input field
                        $currentElement.closest('tr').find('input[name="calculation"]').val(impression);
                        // Clear and append new ad placements
                        $select.empty();
                        $select.append('<option value="">--Select--</option>');

                        $.each(adPlacementList, function (key, value) {
                            $select.append(`<option value="${value}">${value}</option>`);
                        });

                        // Reinitialize select2 with new options
                        $select.select2({
                            placeholder: "--Select--",
                            allowClear: true,
                        });
                    } else {
                        $currentElement.closest('tr').find('input[name="cpm"]').val(0).attr("readonly", false);
                        $currentElement.closest('tr').find('input[name="calculation"]').val('');
                    }

                }
            });
        }
    });

    $(document).on("change", ".site_section", function () {
        var client = $('#client').val();
        var selectedValue = $('#segment').val();
        var $currentElement = $(this); // Store reference to the current .site_section element

        $.ajax({
            url: '[[=URL("default","get_segment_wise_data")]]', // Replace with your endpoint
            method: 'GET',
            data: { client: client, segment: selectedValue },
            dataType: 'json',
            success: function (data) {
                // Assuming data['results'] contains the inventory options
                var deviceList = data['results']['device'];
                //console.log(deviceList);

                // Find the closest row to the changed .site_section element
                var $row = $currentElement.closest('tr');
                var $select2 = $row.find('.adsize');
                $select2.empty();
                // Find the .device select element in the current row
                var $select = $row.find('.device');

                // Clear the existing options
                $select.empty();

                // Add a default option
                $select.append('<option value="">--Select--</option>');

                // Loop through deviceList and append each option
                deviceList.forEach(function (device) {
                    var option = $('<option></option>')
                        .attr("value", device.name) // Assuming 'name' is the value you want
                        .text(device.name);         // Assuming 'name' is the text you want

                    // Append the option to the select element
                    $select.append(option);
                });
            }
        });
    });

    $(document).on("change", ".device", function () {
        var segment = $('#segment').val();
        var ad_type = $('.ad_type').val();
        // var site_section = $(this).val();
        var ad_placement = $(this).closest('tr').find('.site_section').val();
        var device = $(this).closest('tr').find('.device').val();

        //console.log(device)
        //console.log(ad_placement)
        var $select = $(this).closest('tr').find('.adsize')
        $.ajax({
            url: '[[=URL("default","get_segment_adtype_adplacementad_device_wise_size")]]',
            method: 'GET',
            data: { segment: segment, ad_type: ad_type, ad_placement: ad_placement, device: device },
            dataType: 'json',
            success: function (data) {
                // console.log(data['results'])
                $select.empty();
                $select.append('<option value="">Select Ad Size</option>');

                // Append new options
                $.each(data['results'], function (key, value) {
                    $select.append(`<option value="${value.adsize}">${value.adsize}</option>`);
                });

                // Reinitialize select2 with new options
                $select.select2({
                    placeholder: "--Select--",
                    allowClear: true,
                });
            }
        });
    })

    $(document).on("change", ".geo_target", function () {
        var geo_target = $(this).val();
        if (geo_target==='Others'){
            $(this).closest('tr').find('.geo_target_others').show();
        }else{
            $(this).closest('tr').find('.geo_target_others').hide();
        } 
    });

    // Array to store the added records adplacement,device,adsize    
    var trData = '';
    $(document).on("click", ".addQue", function () {
        // Find the closest <tr> to the clicked button
        var row = $(this).closest('table').closest('tr');

        // Now get the value of the ad_type, site_section, device, adsize, and singleRow elements in the row
        var ad_type = row.find('.ad_type').val();
        var site_section = row.find('.site_section').val();
        var device = row.find('.device').val();
        var adsize = row.find('.adsize').val();
        var singleRow = row.find('.singleRow'); // This is the input/textarea element
        var singleRowValue = singleRow.val() || ''; // Get the actual value

        // Check if all fields are filled
        if (ad_type === '' || site_section === '' || device === '' || adsize === '') {
            console.log('All fields are required')
        } else {
            var value = site_section + '<fdfd>' + device + '<fdfd>' + adsize;

            // Check for duplicates in the string
            if (singleRowValue.indexOf(value) > -1) {
                console.log('This record already exists')
            } else {
                // Append the new row with the separator
                if (singleRowValue === '') {
                    singleRowValue = value; // First entry
                } else {
                    singleRowValue += '<rdrd>' + value; // Add subsequent entries with row separator
                }
                // Update the singleRow field with the new value
                singleRow.val(singleRowValue);

            }
        }
        //console.log(singleRowValue);
        var trRec = singleRowValue.split('<rdrd>'); // Split rows by <rdrd>
        var tr = '';
        if (trRec == '') {
            console.log('empty')
        } else {
            // Loop through each row and split by <fdfd> for values
            trRec.forEach(function (row, index) {
                var trRecStr = row.split('<fdfd>'); // Split values by <fdfd>
                tr += '<tr class="' + index + '"><td style="width:136.5px; padding: 2px">' + trRecStr[0] + '</td><td style="width:136.5px; padding: 2px">' + trRecStr[1] + '</td><td style="width:136.5px; padding: 2px">' + trRecStr[2] + '</td><td style="width:29px;  padding: 2px" class="removeQue"><input type="hidden" class="singleRowRemove" value="' + row + '"><a class="text-danger" href="#"><i class="fa-solid fa-circle-minus"></i></a></td></tr>';
            });
        }
        // Clear the table and append the new rows
        row.find('.tableClass').empty();
        row.find('.tableClass').append(tr);

        row.find('.site_section').empty();
        row.find('.adsize').empty();

        row.find('.ad_type').change();

        row.find('.device').empty();
        //var device = row.find('.device').val();
        // var $currentElement = $(this); 
        // $currentElement.closest('tr').find('.device').empty();
        //$(this).parent('tr').remove();  
    });

    //Array to store the remove records adplacement,device,adsize 
    $(document).on("click", ".removeQue", function () {
        // Find the closest <tr> to the clicked button
        var row = $(this).closest('table').closest('tr');
        var row2 = $(this).closest('tr');

        var singleRow = row.find('.singleRow');
        var singleRowValue = singleRow.val() || '';
        var singleRowRemove = row2.find('.singleRowRemove');
        var singleRowRemoveValue = singleRowRemove.val() || ''; // Get the actual value


        // $(this).remove();	
        var listS = '';
        iStrS = singleRowValue.split('<rdrd>');
        iLenS = iStrS.length
        for (i = 0; i < iLenS; i++) {
            if (iStrS[i] != singleRowRemoveValue) {
                if (listS == '') {
                    listS = iStrS[i]
                } else {
                    listS += '<rdrd>' + iStrS[i]
                }
            }
        }
        singleRow.val(listS);

        var trRec = listS.split('<rdrd>'); // Split rows by <rdrd>
        var tr = '';
        if (trRec == '') {
            console.log('empty')
        } else {
            // Loop through each row and split by <fdfd> for values
            trRec.forEach(function (row, index) {
                var trRecStr = row.split('<fdfd>'); // Split values by <fdfd>
                tr += '<tr class="' + index + '"><td style="width:136.5px; padding: 2px">' + trRecStr[0] + '</td><td style="width:136.5px; padding: 2px">' + trRecStr[1] + '</td><td style="width:136.5px; padding: 2px">' + trRecStr[2] + '</td><td style="width:29px;  padding: 2px" class="removeQue"><input type="hidden" class="singleRowRemove" value="' + row + '"><a class="text-danger" href="#"><i class="fa-solid fa-circle-minus"></i></a></td></tr>';
            });
        }
        // Clear the table and append the new rows
        row.find('.tableClass').empty();
        row.find('.tableClass').append(tr);

        //=========
        // $('.ad_type').change();
        row.find('.ad_type').change();
        row.find('.device').empty();
    });

    //=========get segment wise data 
    // $("#segment").on('change', function () {
    //     segmentChange("#tbody tr")
    // });
    function segmentChange(selector) {
        var client = $('#client').val();
        var selectedValue = $('#segment').val();
        if (selectedValue === 'Local') {
            $("#invoiceFile").hide();
            $("#client_creative_files").show();
            $("#landingLink").show();
            $("#primary_final_approval").show();
        } else {
            $("#invoiceFile").show();
            $("#client_creative_files").hide();
            $("#landingLink").hide();
            $("#primary_final_approval").hide();
        }

        if (client === '') {
            Toast.fire({
                // title: "Warning",
                text: "Required client",
                icon: "warning"
            });
            //$('#segment').val('');
            $(".selectChange").each(function () {
                $(this).select2({
                    placeholder: "--Select--",
                    allowClear: true,
                });
            });
        } else if (selectedValue === '') {
            Toast.fire({
                // title: "Warning",
                text: "Required segment",
                icon: "warning"
            });
            $('#segment').val('');
            $(".selectChange").each(function () {
                $(this).select2({
                    placeholder: "--Select--",
                    allowClear: true,
                });
            });
        } else {
            $.ajax({
                url: '[[=URL("default","get_segment_wise_data")]]', // Replace with your endpoint
                method: 'GET',
                data: { client: client, segment: selectedValue },
                dataType: 'json',
                success: function (data) {
                    // Assuming data['results'] contains the inventory options
                    var inventoryList = data['results']['inventory'];
                    var deviceList = data['results']['device'];
                    var geoTargetList = data['results']['geo_target'];
                    var publicationList = data['results']['publication'];
                    var brandList = data['results']['brand'];
                    //var row = $(this).closest('table').closest('tr');
                    //console.log(inventoryList)
                    // Loop through each row in the table ad_type
                    $(selector).each(function () {
                        var $row = $(this);
                        $row.find('.geo_target_others').hide();
                        // Find the .ad_type select element in the current row
                        var $select = $row.find('.ad_type');
                        $row.find('.site_section').empty();
                        $row.find('.adsize').empty();

                        //var tset=$row.find('.singleRow').val('')

                        // Clear the existing options
                        $select.empty();

                        // Add a default option
                        $select.append('<option value="">--Select--</option>');

                        // Loop through inventoryList and append each option
                        inventoryList.forEach(function (inventory) {
                            var option = $('<option></option>')
                                .attr("value", inventory.accpac_id) // Assuming 'inventory_name' is the value you want
                                .text(inventory.inventory_name);         // Assuming 'inventory_name' is the text you want

                            // Append the option to the select element
                            $select.append(option);
                        });
                        //=====================
                        // Find the .device select element in the current row
                        var $select1 = $row.find('.device');

                        // Clear the existing options
                        $select1.empty();

                        // Add a default option
                        $select1.append('<option value="">--Select--</option>');

                        // Loop through deviceList and append each option
                        deviceList.forEach(function (device) {
                            var option = $('<option></option>')
                                .attr("value", device.name) // Assuming 'name' is the value you want
                                .text(device.name);         // Assuming 'name' is the text you want

                            // Append the option to the select element
                            $select1.append(option);
                        });
                        //=====================
                        // Find the .geo_target select element in the current row
                        var $select2 = $row.find('.geo_target');

                        // Clear the existing options
                        $select2.empty();

                        // Add a default option
                        $select2.append('<option value="">--Select--</option>');

                        // Loop through geoTargetList and append each option
                        geoTargetList.forEach(function (geo_target) {
                            var option = $('<option></option>')
                                .attr("value", geo_target.geo_name) // Assuming 'geo_name' is the value you want
                                .text(geo_target.geo_name);         // Assuming 'geo_name' is the text you want

                            // Append the option to the select element
                            $select2.append(option);
                        });
                        //=====================
                        // Find the .publication select element in the current row
                        var $select3 = $row.find('.publication');

                        // Clear the existing options
                        $select3.empty();

                        // Add a default option
                        $select3.append('<option value="">--Select--</option>');

                        // Loop through publicationList and append each option
                        publicationList.forEach(function (publication) {
                            var option = $('<option></option>')
                                .attr("value", publication.name) // Assuming 'name' is the value you want
                                .text(publication.name);         // Assuming 'name' is the text you want

                            // Append the option to the select element
                            $select3.append(option);
                        });
                        //=====================
                        // Find the .brand select element in the current row
                        var $select4 = $row.find('.brand');

                        // Clear the existing options
                        $select4.empty();

                        // Add a default option
                        $select4.append('<option value="">--Select--</option>');

                        // Loop through brandList and append each option
                        brandList.forEach(function (brand) {
                            console.log(brand.id)
                            var option = $('<option></option>')
                                .attr("value", brand.id) // Assuming 'brand_name' is the value you want
                                .text(brand.brand_name);         // Assuming 'brand_name' is the text you want

                            // Append the option to the select element
                            $select4.append(option);
                        });

                    });

                }
            });
        }

    }

    //=========special discount calculation
    // $("#special_discount").on('keyup blur', function () {
    //     specialDiscount();
    // })
    // function specialDiscount() {
    //     var sub_total = $("#sub_total").val();
    //     var discount_total = $("#discount_total").val();
    //     var special_discount = $("#special_discount").val();
    //     var vatPercent = parseInt($("#vatPercent").val());
    //     if (special_discount == '') {
    //         special_discount = 0
    //     }
    //     var total_discount = parseInt(discount_total) + parseInt(special_discount)
    //     var totalVatableAmount = Math.round((sub_total - total_discount))
    //     var vat_amount = Math.round(totalVatableAmount * vatPercent / 100)
    //     var net_amount = totalVatableAmount + vat_amount

    //     $("#vatable_amount").html(totalVatableAmount.toLocaleString());
    //     $("#total_vatable_amount").val(totalVatableAmount);

    //     $("#vat").html(vat_amount.toLocaleString());
    //     $("#vat_amount").val(vat_amount);

    //     $("#net_total").html(net_amount.toLocaleString());
    //     $("#net_total_amount").val(net_amount);
    // };

