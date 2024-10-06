document.getElementById('settingsForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // 阻止表单的默认提交行为

    const formData = new FormData(event.target);

    try {
        const response = await fetch('/admin', {
            method: 'POST',
            body: formData,
        });

        // 确保服务器的响应是成功的
        if (response.ok) {
            alert("设置更新成功！"); // 可以自定义提示消息
            location.reload(); // 刷新当前页面
        } else {
            alert("设置更新失败，请重试。"); // 处理错误情况
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        alert("请求失败，请重试。");
    }
});