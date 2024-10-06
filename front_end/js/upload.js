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

fileUploader.addEventListener('drop', (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files; // 更新文件输入控件的文件
        console.log('拖放文件上传:', file.name);
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

// 处理复制取件链接按钮的点击事件
copyLinkButton.addEventListener('click', (e) => {
    e.preventDefault(); // 阻止默认行为
    const link = pickupLinkElement.href;
    navigator.clipboard.writeText(link).then(() => {
        alert('取件链接已复制到剪切板: ' + link);
    }).catch(err => {
        alert('无法复制到剪切板: ' + err);
    });
});

pickupCodeButton.addEventListener('click', (e) => {
    e.preventDefault(); // 阻止默认行为
    navigator.clipboard.writeText(code).then(() => {
        alert('取件码已复制到剪切板: ' + code);
    }).catch(err => {
        alert('无法复制到剪切板: ' + err);
    });
});

pickupCodeButton.addEventListener('click', (e) => {
    e.preventDefault(); // 阻止默认行为
    const code = result.code;
    navigator.clipboard.writeText(code).then(() => {
        alert('取件码已复制到剪切板: ' + code);
    }).catch(err => {
        alert('无法复制到剪切板: ' + err);
    });
});
async function autoUpload(file, chunk_size = 30 * 1024 * 1024) {
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

    for (let i = 0; i < totalChunks; i++) {
        const chunk = file.slice(start, Math.min(start + chunk_size, file.size)); // 获取当前块
        await upload_chunk(chunk, i);
        start = start + chunk_size;
    }

    const response2 = await fetch('/mergechunk/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code, expiration: selectElement.value }) // 将 code 作为请求体发送
    });

    if (!response2.ok) {
        throw new Error('网络响应不符合预期');
    }
    else {
        document.getElementById('fileInfo').textContent = '已上传文件名：' + file.name;
        document.querySelector('.right-section').style.display = 'flex';
        document.querySelector('.left-section').style.display = 'flex';
        pickupCodeButton.innerText = '取件码: ' + code;
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