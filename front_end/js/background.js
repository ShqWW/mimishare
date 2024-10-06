// async function setBackground() {
//     try {
//         const response = await fetch('/background');
//         const data = await response.json();
//         document.body.style.backgroundImage = `url('${data.url}')`;
//         document.body.classList.add('loaded'); // 加载完成后添加类
//     } catch (error) {
//         console.error('Error fetching background image:', error);
//         document.body.classList.add('loaded'); // 即使出错也显示页面
//     }
// }
// // setBackground();
// window.onload = setBackground; // 页面加载完成后执行背景图设置
