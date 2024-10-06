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
            }
        })
        .catch(error => {
            console.error('删除请求出错:', error);
            alert('删除请求出错，请重试。');
        });
}