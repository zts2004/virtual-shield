const fs = require('fs');
const path = require('path');

// 定义文件夹列表
const folders = ['附件一', '附件二', '附件三', '附件四', '视频'];

// 获取文件类型
function getFileType(fileName) {
    const ext = path.extname(fileName).toLowerCase().slice(1);
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

// 更新单个文件夹的JSON文件
function updateFolderJson(folderName) {
    const folderPath = path.join('files', folderName);
    const jsonPath = path.join(folderPath, 'index.json');

    // 确保文件夹存在
    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, { recursive: true });
    }

    // 读取文件夹中的所有文件
    fs.readdir(folderPath, (err, files) => {
        if (err) {
            console.error(`读取文件夹 ${folderName} 时出错:`, err);
            return;
        }

        // 过滤掉 index.json 文件
        files = files.filter(file => file !== 'index.json');

        // 创建文件列表
        const fileList = files.map(file => ({
            name: file,
            path: file,
            type: getFileType(file)
        }));

        // 写入 JSON 文件
        fs.writeFile(jsonPath, JSON.stringify(fileList, null, 4), 'utf8', (err) => {
            if (err) {
                console.error(`更新 ${folderName} 的 index.json 时出错:`, err);
            } else {
                console.log(`已更新 ${folderName} 的文件列表`);
            }
        });
    });
}

// 更新所有文件夹
folders.forEach(folder => {
    updateFolderJson(folder);
});

// 设置文件系统监视器
folders.forEach(folder => {
    const folderPath = path.join('files', folder);
    fs.watch(folderPath, (eventType, filename) => {
        if (filename && filename !== 'index.json') {
            console.log(`检测到 ${folder} 文件夹中的变化:`, eventType, filename);
            updateFolderJson(folder);
        }
    });
});

console.log('文件监视器已启动，正在监控文件夹变化...'); 