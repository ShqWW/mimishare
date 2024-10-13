document.addEventListener('DOMContentLoaded', function () {
    var fileNames = document.querySelectorAll('.file-name');
    let fileExtension, iconInfo, iconClass, iconColor;
    fileNames.forEach(function (fileNameElement) {
        var fileName = fileNameElement.getAttribute('data-file');
        var fileIcon = document.createElement('i');
        fileExtension = fileName.split('.').pop().toLowerCase();

        // if (fileName.endsWith('.jpg') || fileName.endsWith('.png') || fileName.endsWith('.gif')) {
        //     fileIcon.className = 'fa-solid fa-file-image';
        // } else if (fileName.endsWith('.pdf')) {
        //     fileIcon.className = 'fa-solid fa-file-pdf';
        // } else if (fileName.endsWith('.doc') || fileName.endsWith('.docx')) {
        //     fileIcon.className = 'fa-solid fa-file-word';
        // } else if (fileName.endsWith('.xls') || fileName.endsWith('.xlsx')) {
        //     fileIcon.className = 'fa-solid fa-file-excel';
        // } else if (fileName.endsWith('.ppt') || fileName.endsWith('.pptx')) {
        //     fileIcon.className = 'fa-solid fa-file-powerpoint';
        // } else if (fileName.endsWith('.zip') || fileName.endsWith('.rar') || fileName.endsWith('.tar') || fileName.endsWith('.gz')) {
        //     fileIcon.className = 'fa-solid fa-file-archive';
        // } else if (fileName.endsWith('.mp4') || fileName.endsWith('.avi') || fileName.endsWith('.mkv')) {
        //     fileIcon.className = 'fa-solid fa-file-video';
        // } else if (fileName.endsWith('.mp3') || fileName.endsWith('.wav') || fileName.endsWith('.ogg') || fileName.endsWith('.gz')) {
        //     fileIcon.className = 'fa-solid fa-file-audio';
        // } else if (fileName.endsWith('.txt')) {
        //     fileIcon.className = 'fa-solid fa-file-lines';
        // } else {
        //     fileIcon.className = 'fa-solid fa-file';
        // }
        iconInfo = select_icon(fileExtension);
        console.log(iconInfo.iconClass);
        iconClass = iconInfo.iconClass; // 获取图标类
        iconColor = iconInfo.iconColor; // 获取图标颜色

        fileIcon.className = iconClass

        // fileNameElement.insertBefore(fileIcon, fileNameElement.firstChild);
        fileNameElement.innerHTML = `<i class="${iconClass}" style="color: ${iconColor}; margin-right: 5px;"></i> ${fileName}`;
    });
});