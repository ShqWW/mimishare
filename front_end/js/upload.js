const fileUploader = document.getElementById('fileUploader');
const fileInput = document.getElementById('fileInput');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const pickupCodeButton = document.getElementById('pickupCodeButton');
const pickupLinkElement = document.getElementById('pickupLink');
const copyLinkButton = document.getElementById('copyLinkButton');
// 获取 select 元素
const selectElement = document.getElementById('expiration');
let result;
let code;
// 允许拖放文件到指定区域
fileUploader.addEventListener('dragover', (e) => {
    e.preventDefault();
});
// document.getElementById('send-container').style.display='none';
// document.getElementById('share-container').style.display='none';
var qr = new QRious({
    element: document.getElementById('qrCanvas'),
    value: "afsdfasfsfgesgsdfgsfdgsgsgsgsgsggsgsg", // 在这里放入取件码
    foreground: 'white', // 设置前景颜色为白色
    background: 'transparent',
    size: 100
});

fileUploader.addEventListener('drop', (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files; // 更新文件输入控件的文件
        if (file.size <= sizeLimitMB * 1024 * 1024) { // 20MB
            autoUpload(file, chunksize * 1024 * 1024); // 自动上传文件
        } else {
            alert(`文件大小超过${sizeLimitMB}MB，请选择较小的文件。`);
        }
    }
});

// 文件选择后执行上传操作
fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        if (file.size <= sizeLimitMB * 1024 * 1024) { // 20MB
            autoUpload(file, chunksize * 1024 * 1024); // 自动上传文件
        } else {
            alert(`文件大小超过${sizeLimitMB}MB，请选择较小的文件。`);
        }
    }
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

// function captureElement() {
//     html2canvas(document.querySelector("#hijk")).then(canvas => {
//         // 创建一个新的 a 标签，用于下载图片
//         const link = document.createElement("a");
//         link.href = canvas.toDataURL();
//         link.download = "share-card.png";
//         link.click();
//     });
// }



async function autoUpload(file, chunk_size = 30 * 1024 * 1024) {
    document.getElementById('send-container').style.display='none';
    document.getElementById('share-container').style.display='none';
    // 显示进度条
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    let start = 0;
    const totalChunks = Math.ceil(file.size / chunk_size);
    const response = await fetch('/generatecode/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: file.name })
    });

    // 检查响应是否成功
    if (!response.ok) {
        alert('请求失败: ' + response.statusText);
        throw new Error('网络响应失败');
    }

    // 解析响应的 JSON 数据
    const data = await response.json();
    code = data.code;
    // alert(code);

    async function upload_chunk(chunk, i) {
        return new Promise((resolve, reject) => {
            const formData = new FormData();
            formData.append("file", chunk);
            formData.append("code", code);
            formData.append("index", i);
            formData.append("total_chunks", totalChunks);
            const xhr = new XMLHttpRequest();
            // 进度监听
            xhr.upload.addEventListener('progress', function (event) {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * (100 / totalChunks); // 计算整体进度
                    progressBar.style.width = `${percentComplete + (i * (100 / totalChunks))}%`; // 更新进度条
                }
            });

            // 响应处理
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        resolve(); // 成功上传，解决 Promise
                    } else {
                        const result = JSON.parse(xhr.responseText);
                        alert("文件上传失败: " + result.info);
                        reject(new Error("Upload failed")); // 失败时拒绝 Promise
                    }
                }
            };

            // 发送请求
            xhr.open("POST", "/uploadchunk/");
            xhr.send(formData);
        });
    }

    
    async function mergechunk() {
        const response_merge = await fetch('/mergechunk/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code, expiration: selectElement.value}) // 将 code 作为请求体发送
        });

        if (!response_merge.ok) {
            throw new Error('网络响应不符合预期');
        }
        else {
            const data_merge = await response_merge.json();
            const deadline = data_merge.deadline;
            const filesize = data_merge.filesize;

            setFileInfo(file.name);
            document.getElementById('send-container').style.display='none';
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
            fileInput.value = ''
        }
    }
    for (let i = 0; i < totalChunks; i++) {
        const chunk = file.slice(start, Math.min(start + chunk_size, file.size)); // 获取当前块
        await upload_chunk(chunk, i);
        start = start + chunk_size;
    }
    document.getElementById('send-container').style.display='block';
    document.getElementById('filetitle-send').innerHTML = `<i class="fa-solid fa-upload" style="color: #66a8ff; font-size: 25px; margin-right:5px;"></i> ${file.name}`;
    document.getElementById('filetitle-send').title = file.name;
    document.getElementById('uploadButton').onclick = mergechunk;
    // document.getElementById('mmmbtn').onclick = captureElement;
    // mergechunk();
    
    
}