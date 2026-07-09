#!/bin/bash
# Arrowmatics ai sdn bhd - Quick GitHub Deployment Script
# Run this after creating your GitHub repository

echo "📦 Creating deployment package..."
cd C:/Users/Admin/Documents/HermesWorkspace/Innovator1

# Create ZIP file for easy upload
zip -r arrowmatics-magnets.zip *.html *.xml *.md images/

echo "✅ Created arrowmatics-magnets.zip"
echo ""
echo "🚀 DEPLOYMENT STEPS:"
echo "1. Go to https://github.com/new"
echo "2. Create repository: arrowmatics-magnets"
echo "3. Click 'Upload files'"
echo "4. Drag arrowmatics-magnets.zip"
echo "5. Extract files after upload"
echo "6. Go to Settings > Pages"
echo "7. Select Source: main branch / (root)"
echo "8. Click Save"
echo ""
echo "🌐 Your site will be live at:"
echo "   https://YOUR-USERNAME.github.io/arrowmatics-magnets/"