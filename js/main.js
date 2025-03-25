// 获取当前日期并格式化为YYYYMMDD格式
function getCurrentPassword() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    return `${year}${month}${day}`;
}

// 验证密码
function verifyPassword() {
    const passwordInput = document.getElementById('password-input');
    const currentPassword = getCurrentPassword();
    
    if (passwordInput.value === currentPassword) {
        // 密码正确，显示主界面
        document.getElementById('password-screen').classList.add('hidden');
        document.getElementById('main-screen').classList.remove('hidden');
        // 将验证状态存储在sessionStorage中
        sessionStorage.setItem('verified', 'true');
    } else {
        alert('密码错误，请重试！');
        passwordInput.value = '';
    }
}

// 检查是否已经验证过
function checkVerification() {
    if (sessionStorage.getItem('verified') === 'true') {
        document.getElementById('password-screen').classList.add('hidden');
        document.getElementById('main-screen').classList.remove('hidden');
    }
}

// 获取文件类型
function getFileType(fileName) {
    const ext = fileName.split('.').pop().toLowerCase();
    const typeMap = {
        'pdf': 'pdf',
        'doc': 'doc',
        'docx': 'docx',
        'xls': 'xls',
        'xlsx': 'xlsx',
        'jpg': 'jpg',
        'jpeg': 'jpeg',
        'png': 'png',
        'mp4': 'mp4'
    };
    return typeMap[ext] || 'default';
}

// 打开文件夹预览
async function openFile(folderName) {
    try {
        // 显示预览界面
        showPreview(folderName);
    } catch (err) {
        console.error('无法访问文件夹:', err);
        alert('无法访问文件夹，请稍后重试。');
    }
}

// 显示预览界面
function showPreview(folderName) {
    // 创建预览模态框
    const modal = document.createElement('div');
    modal.className = 'preview-modal';
    modal.innerHTML = `
        <div class="preview-content">
            <div class="preview-header">
                <h2>${folderName}</h2>
                <button class="close-btn" onclick="this.parentElement.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="preview-body">
                <div class="file-list">
                    <div class="loading">加载中...</div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    // 加载文件列表
    loadFiles(folderName, modal.querySelector('.file-list'));
}

// 加载文件列表
async function loadFiles(folderName, container) {
    try {
        container.innerHTML = '<div class="loading">加载中...</div>';
        // 从GitHub仓库读取index.json文件
        const response = await fetch(`https://raw.githubusercontent.com/zts2004/virtual-shield/main/files/${folderName}/index.json`);
        
        if (!response.ok) {
            throw new Error('无法加载文件列表');
        }
        
        const data = await response.json();
        const files = data.files || [];
        
        if (files.length === 0) {
            container.innerHTML = '<div class="no-files">文件夹为空</div>';
            return;
        }
        
        container.innerHTML = files.map(file => `
            <div class="file-item" onclick="previewFile('${folderName}/${file.name}')">
                <div class="file-icon">${getFileIcon(file.type)}</div>
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('加载文件列表失败:', error);
        container.innerHTML = `
            <div class="error">
                <div class="error-message">无法加载文件列表</div>
                <div class="error-details">${error.message}</div>
                <button onclick="loadFiles('${folderName}', this.parentElement)">重试</button>
            </div>
        `;
    }
}

// 获取文件图标
function getFileIcon(fileType) {
    const icons = {
        'pdf': '📄',
        'doc': '📝',
        'docx': '📝',
        'xls': '📊',
        'xlsx': '📊',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
        'mp4': '🎥',
        'default': '📁'
    };
    return icons[fileType] || icons.default;
}

// 预览文件
function previewFile(filePath) {
    const fileType = filePath.split('.').pop().toLowerCase();
    const previewWindow = window.open('', '_blank');
    
    // 使用GitHub原始文件URL
    const fileUrl = `https://raw.githubusercontent.com/zts2004/virtual-shield/main/files/${filePath}`;
    
    if (['jpg', 'jpeg', 'png'].includes(fileType)) {
        previewWindow.document.write(`
            <html>
                <head>
                    <title>图片预览</title>
                    <style>
                        body { margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #000; }
                        img { max-width: 100%; max-height: 100vh; }
                    </style>
                </head>
                <body>
                    <img src="${fileUrl}" alt="预览图片">
                </body>
            </html>
        `);
    } else if (fileType === 'pdf') {
        previewWindow.document.write(`
            <html>
                <head>
                    <title>PDF预览</title>
                    <style>
                        body { margin: 0; height: 100vh; }
                        iframe { width: 100%; height: 100%; border: none; }
                    </style>
                </head>
                <body>
                    <iframe src="${fileUrl}"></iframe>
                </body>
            </html>
        `);
    } else if (fileType === 'mp4') {
        previewWindow.document.write(`
            <html>
                <head>
                    <title>视频预览</title>
                    <style>
                        body { margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #000; }
                        video { max-width: 100%; max-height: 100vh; }
                    </style>
                </head>
                <body>
                    <video controls>
                        <source src="${fileUrl}" type="video/mp4">
                        您的浏览器不支持视频播放
                    </video>
                </body>
            </html>
        `);
    } else {
        previewWindow.document.write(`
            <html>
                <head>
                    <title>文件预览</title>
                    <style>
                        body { margin: 20px; font-family: Arial, sans-serif; }
                        .download-btn {
                            display: inline-block;
                            padding: 10px 20px;
                            background: #4CAF50;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                        }
                    </style>
                </head>
                <body>
                    <h2>此文件类型暂不支持预览</h2>
                    <a href="${fileUrl}" class="download-btn" download>下载文件</a>
                </body>
            </html>
        `);
    }
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 页面加载时检查验证状态
document.addEventListener('DOMContentLoaded', checkVerification);

// 添加回车键验证功能
document.getElementById('password-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        verifyPassword();
    }
}); 