const pickupCodeButton = document.getElementById('pickupCodeButton');
const pickupLinkElement = document.getElementById('pickupLink');
const copyLinkButton = document.getElementById('copyLinkButton');
const selectTime = document.getElementById('expiration');
const selectFile = document.getElementById('filename');
let result;
let code;

function copyCode(button) {
    const tempInput = document.createElement('input');
    const code = button.code;
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

async function autoUpload() {
    const response = await fetch('/servershareaction/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: selectFile.value, expiration: selectTime.value })
    });

    if (!response.ok) {
        alert('请求失败: ' + response.statusText);
        throw new Error('网络响应失败');
    } else {
        const data = await response.json();
        code = data.code;
        console.log(code);
        document.getElementById('fileInfo').textContent = '已上传文件名：' + selectFile.value;
        document.querySelector('.right-section').style.display = 'flex';
        document.querySelector('.left-section').style.display = 'flex';
        pickupCodeButton.innerText = code;
        pickupCodeButton.code = code;
        pickupLinkElement.href = 'download/' + code; // 更新为新的取件链接

        // 生成二维码
        var qr = new QRious({
            element: document.getElementById('qrCanvas'),
            value: pickupLinkElement.href,
            foreground: 'white',
            background: 'transparent',
            size: 200 // 设置二维码的大小
        });
    }
}

document.getElementById('uploadButton').addEventListener('click', () => {
    if (selectFile.value === "") { // 使用 === 进行比较
        alert("请先选择一个文件!");
    } else {
        autoUpload();
    }
});