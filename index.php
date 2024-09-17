<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weng's DaVinci Scripter</title>
    <link href="//cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.1/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

    <script>
        function hydrate() {
            document.querySelectorAll('.copy-icon').forEach(function(icon) {
                icon.addEventListener('click', function(event) {
                    event.stopPropagation();
                    event.preventDefault();

                    // Get the corresponding content
                    var content = this.closest(".card").querySelector(".card-text").textContent;

                    // Create a temporary input element to hold the content
                    var tempInput = document.createElement('textarea');
                    tempInput.value = content;
                    document.body.appendChild(tempInput);

                    // Select the text and copy it
                    tempInput.select();
                    document.execCommand('copy');

                    // Remove the temporary input element
                    document.body.removeChild(tempInput);
                    
                    // Close the details element
                    const details = this.closest("details")
                    details.open = false;
                    $(details).removeClass("bg-gray-200").addClass("bg-gray-100");

                    // Provide feedback (optional)
                    // alert('Content copied to clipboard!');

                    // Show the "Copied to clipboard" notification
                    var notification = document.getElementById('copy-notification');
                    notification.classList.remove('hidden');

                    // Hide the notification after 2 seconds
                    setTimeout(function() {
                        notification.classList.add('hidden');
                    }, 2000);

                }); // click
            }); // forEach
        } // hydrate

        let template = "";

        fetch("./fusions/test.lua")
        .then(response=>response.text())
        .then(response => {
            template = response;

            // Presets into webpage
            [
                ["blc", 23, 5],
                ["blc", 23, 5]
            ].forEach((clipData, index) => {
                const [preset, clipFps, clipSeconds] = clipData;
                const clipTemplate = template
                    .replaceAll("_END_FRAME_", parseInt(clipSeconds*clipFps))
                    .replaceAll("_TRNX_", 0.2)
                    .replaceAll("_POS_", -0.2)
                    .replaceAll("_ZOOM_", 1.4);
                console.log(clipTemplate);
                
                $("#results").append(`<details class="bg-gray-200 p-4 m-4">
                    <summary>${clipData.toString()}</summary>

                    <div class="container mt-5">
                        <div class="card">
                            <div class="card-header d-flex justify-content-between align-items-center inline w-fit border border-gray-300 w-fit" style="width:fit-content !important;">
                                <i class="fas fa-copy text-3xl copy-icon" style="cursor: pointer;" title="Copy to clipboard"></i>
                            </div>
                            <div class="card-body">
                                <code id="card-content" class="card-text whitespace-pre-wrap">${clipTemplate}</code>
                            </div>
                        </div>
                    </div>

                </details>
                `); // append

                hydrate();

            });
        });
    </script>
</head>
<body>
    <div class="container mt-4">
        <h1>Weng's DaVinci Scripter</h1>
        <main id="results"></main>
    </div>

    <!-- Notification -->
    <div id="copy-notification" class="hidden fixed bottom-4 right-4 bg-green-100 text-green-600 px-4 py-2 rounded shadow-lg opacity-70">
        Copied to clipboard!
    </div>
</body>
</html>