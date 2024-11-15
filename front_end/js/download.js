// script.js

document.getElementById('pickupCode').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // 防止回车键触发默认行为（例如表单提交）
        document.querySelector('.input-container button').click(); // 触发下载文件按钮的点击事件
    }
});
document.getElementById('fetch-result').style.display='none';

async function fetchFile() {
    const pickupCode = document.getElementById('pickupCode').value;
    if (!pickupCode) {
        alert('请填写取件码');
        return;
    }

    const response = await fetch(`/fetchfile/${pickupCode}`);

    if (!response.ok) {
        const error = await response.json();
        alert(error.detail);  // 弹出错误信息
        return;
    }

    const fileInfo = await response.json();


    document.getElementById('fetch-result').style.display='block';

    // document.getElementById('file-name').innerText = `文件名称: ${fileInfo.filename}`;
    setFileInfo(fileInfo.name)
    // document.getElementById('file-size').innerText = `文件大小: ${fileInfo.filesize}`;
    document.getElementById('file-size').innerHTML = `<i class="fa-solid fa-hard-drive" style="color: #66a8ff; font-size: 18px; margin-right:5px;"></i> 文件大小: ${fileInfo.filesize}`;
    document.getElementById('pickupLink').href = `/download/${pickupCode}`;
    
}





async function downloadFile() {
    const pickupCode = document.getElementById('pickupCode').value;

    if (!pickupCode) {
        alert('请填写取件码');
        return;
    }

    try {
        const response = await fetch(`/download/${pickupCode}`);

        if (!response.ok) {
            const error = await response.json();
            alert(error.detail);  // 弹出错误信息
            return;
        }

        // 创建一个Blob URL并下载文件
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;

        // 获取文件名并设置为下载时的文件名
        const contentDisposition = response.headers.get('Content-Disposition');
        const fileName = contentDisposition ? contentDisposition.split('filename=')[1].replace(/"/g, '') : `${pickupCode}.download`;
        a.download = fileName;  // 设置下载文件名
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        alert('下载过程中出现错误，请重试。');  // 通用错误消息
    }
}