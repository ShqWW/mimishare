function confirmDelete(code) {
    // 使用 fetch 发送删除请求
    fetch(`/delete/${code}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => {
            if (response.ok) {
                // 删除成功后更新页面
                location.reload();
            } else {
                alert('删除失败，请重试。');
                location.reload();
            }
        })
        .catch(error => {
            console.error('删除请求出错:', error);
            alert('删除请求出错，请重试。');
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // 获取所有canvas元素
    const qrCanvases = document.querySelectorAll('.qrCanvas');

    // 遍历每个canvas，生成QR码
    qrCanvases.forEach(canvas => {
        const qr = new QRious({
            element: canvas,
            value: canvas.getAttribute('data-code'), // 取件码
            foreground: 'white', // 设置前景颜色为白色
            background: 'transparent'
        });
    });
});


function copyCode(code) {
    const tempInput = document.createElement('input');
    tempInput.value = code;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    alert('取件码已复制到剪贴板：' + code);
}



function copyLink(event, button) {
    event.preventDefault(); // 阻止默认的下载行为
    const tempInput = document.createElement('input');
    tempInput.value = button.parentElement.href;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    alert('下载链接已复制到剪贴板：' + button.parentElement.href);
}