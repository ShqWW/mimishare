function select_icon(extension){
    let iconClass;
    let iconColor;
    switch (extension) {
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
            iconClass = 'fa-solid fa-file-image';
            iconColor = '#ff6666'; // 图片文件的图标颜色
            break;
        case 'pdf':
            iconClass = 'fa-solid fa-file-pdf';
            iconColor = '#ff4040'; // PDF文件的图标颜色
            break;
        case 'doc':
        case 'docx':
            iconClass = 'fa-solid fa-file-word';
            iconColor = '#4096ff'; // Word文件的图标颜色
            break;
        case 'xls':
        case 'xlsx':
            iconClass = 'fa-solid fa-file-excel';
            iconColor = '#00b359'; // Excel文件的图标颜色
            break;
        case 'ppt':
        case 'pptx':
            iconClass = 'fa-solid fa-file-powerpoint';
            iconColor = '#ff8000'; // PowerPoint文件的图标颜色
            break;
        case 'zip':
        case 'rar':
        case 'tar':
        case '.gz':
            iconClass = 'fa-solid fa-file-zipper';
            iconColor = '#8c8c8c'; // 压缩文件的图标颜色
            break;
        case 'mp4':
        case 'avi':
        case 'mkv':
            iconClass = 'fa-solid fa-file-video';
            iconColor = '#0066ff'; // 视频文件的图标颜色
            break;
        case 'mp3':
        case 'wav':
        case 'ogg':
            iconClass = 'fa-solid fa-file-audio';
            iconColor = '#ffcc00'; // 音频文件的图标颜色
            break;
        case 'txt':
            iconClass = 'fa-solid fa-file-lines';
            iconColor = '#009933'; // 文本文件的图标颜色
            break;
        default:
            iconClass = 'fa-solid fa-file';
            iconColor = '#999'; // 文本文件的图标颜色
            break;
    }
    return {iconClass, iconColor}
}

function setFileInfo(filename) {
    let iconClass;
    let iconColor = '#66a8ff'; // 默认颜色
    let iconSize = '25px'; // 默认大小
    // 根据文件后缀选择图标
    const fileExtension = filename.split('.').pop().toLowerCase();
    const iconInfo = select_icon(fileExtension); // 获取图标信息
    iconClass = iconInfo.iconClass; // 获取图标类
    iconColor = iconInfo.iconColor; // 获取图标颜色

    // 设置文件信息
    const fileInfoElement = document.getElementById('filetitle-share');
    fileInfoElement.innerHTML = `<i class="${iconClass}" style="color: ${iconColor}; font-size: ${iconSize}; margin-right: 5px;"></i> ${filename}`;
    fileInfoElement.title = filename; 
}

