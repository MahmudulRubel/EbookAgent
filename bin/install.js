#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('📚 Installing custom-epub-creator AI Skill...\n');

const homeDir = process.env.HOME || process.env.USERPROFILE;
const isLocal = process.argv.includes('--local') || process.argv.includes('-l');

let targetDir;
if (isLocal) {
  targetDir = path.resolve(process.cwd(), '.agents', 'skills', 'custom-epub-creator');
  console.log('📍 Target: Project Workspace (.agents/skills)');
} else {
  targetDir = path.join(homeDir, '.gemini', 'config', 'skills', 'custom-epub-creator');
  console.log('📍 Target: Global AI Skills (~/.gemini/config/skills)');
}

try {
  if (fs.existsSync(targetDir)) {
    console.log('🔄 Cleaning existing skill directory...');
    fs.rmSync(targetDir, { recursive: true, force: true });
  }

  fs.mkdirSync(targetDir, { recursive: true });

  const repoUrl = 'https://github.com/MahmudulRubel/Custom-ePub-Creator.git';
  console.log(`📥 Cloning from ${repoUrl}...`);
  execSync(`git clone ${repoUrl} "${targetDir}"`, { stdio: 'inherit' });

  console.log('\n✨ custom-epub-creator skill successfully installed!');
  console.log(`📁 Location: ${targetDir}\n`);
  console.log('🚀 You can now ask your AI assistant to create ePub & Kindle PDF books!');
} catch (err) {
  console.error('\n❌ Installation failed:', err.message);
  process.exit(1);
}
