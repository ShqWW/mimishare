const pickupCodeButton = document.getElementById('pickupCodeButton');
const pickupLinkElement = document.getElementById('pickupLink');
const copyLinkButton = document.getElementById('copyLinkButton');
const selectTime = document.getElementById('expiration');
const selectFile = document.getElementById('filename');
let result;
let code;
let name_record = null;

var qr = new QRious({
    element: document.getElementById('qrCanvas'),
    value: "afsdfasfsfgesgsdfgsfdgsgsgsgsgsggsgsg", // 在这里放入取件码
    foreground: 'white', // 设置前景颜色为白色
    background: 'transparent',
    size: 100
});

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
    const filename = selectFile.value
    if (filename==name_record)
    {
        alert('不要重复提交！');
        return;
    }
    const response = await fetch('/servershareaction/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({filename: filename, expiration: selectTime.value})
    });

    if (!response.ok) {
        alert('请求失败: ' + response.statusText);
        throw new Error('网络响应失败');
    } 
    else {
        const data = await response.json();
        const code = data.code;
        const deadline = data.deadline;
        const filesize = data.filesize;
        name_record = filename;

        setFileInfo(filename);
        document.getElementById('share-container').style.display='block';
        document.getElementById('filesize').innerHTML = `<i class="fa-solid fa-hard-drive" style="color: #66a8ff; margin-right:5px;"></i> 文件大小: ${filesize}`;
        document.getElementById('deadline').innerHTML = `<i class="fa-regular fa-clock" style="color: #B197FC; margin-right:5px;"></i> 过期时间: ${deadline}`; 
        pickupCodeButton.innerText = code;
        pickupCodeButton.code = code;
        pickupCodeButton.href = code;
        pickupLinkElement.href = 'download/' + code; // 更新为新的取件链接

        // 生成二维码
        var qr = new QRious({
            element: document.getElementById('qrCanvas'),
            value: pickupLinkElement.href, // 在这里放入取件码
            foreground: 'white', // 设置前景颜色为白色
            background: 'transparent'
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