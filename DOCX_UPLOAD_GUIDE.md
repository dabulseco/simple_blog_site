# DOCX Upload Feature Guide

## Overview

The blog system now supports uploading `.docx` (Microsoft Word) files directly! No need to write HTML anymore - just create your blog post in Word with all your formatting, then upload it.

## 🎯 Features

- ✅ **Upload formatted Word documents** (.docx files)
- ✅ **Automatic HTML conversion** with formatting preserved
- ✅ **Live preview** before saving
- ✅ **View HTML source** to see what will be saved
- ✅ **Auto-generate excerpts** from document content
- ✅ **Supports all Word formatting**: headings, bold, italic, lists, tables, images
- ✅ **Bootstrap styling** automatically applied for responsive design

## 📝 How to Use

### Step 1: Prepare Your Document in Word

Create your blog post in Microsoft Word with your preferred formatting:

**Supported Formatting:**
- ✅ Headings (Heading 1, 2, 3)
- ✅ Paragraphs
- ✅ **Bold** and *italic* text
- ✅ Bullet lists and numbered lists
- ✅ Images (embedded in document)
- ✅ Tables
- ✅ Blockquotes
- ✅ Hyperlinks
- ✅ Font colors and highlighting

**Best Practices:**
1. Use Word's built-in **Heading styles** (Heading 1, Heading 2, etc.)
2. Keep images optimized (< 1MB each)
3. Use standard fonts (Arial, Times New Roman, Calibri)
4. Avoid complex formatting like text boxes or WordArt
5. Save as `.docx` format (not .doc)

### Step 2: Upload to Admin Dashboard

1. Open the Admin Dashboard: `streamlit run admin_dashboard.py`
2. Navigate to **"Create New Post"**
3. Fill in basic information:
   - Post Title
   - Category
   - Publication Date
   - Header Image (upload or URL)
4. Under **"Full Article Content"**, select **"Upload DOCX File"**
5. Click **"Browse files"** and select your .docx file
6. Wait for conversion (usually 1-2 seconds)

### Step 3: Preview & Review

After upload, you'll see:

1. **Success Message** - Confirms conversion completed
2. **Two Preview Tabs:**
   - **Visual Preview** - How it will look on your blog
   - **HTML Source** - The generated HTML code
3. **Auto-generated Excerpt** - Suggested summary text

**Review checklist:**
- ✅ All headings converted correctly
- ✅ Formatting preserved (bold, italic, lists)
- ✅ Images displaying properly
- ✅ Tables formatted correctly
- ✅ Links working

### Step 4: Adjust & Save

1. **Excerpt**: Either use the auto-generated one or write your own
2. **Make edits**: If needed, you can:
   - Re-upload a different version
   - Switch to "Write HTML" to manually edit
3. **Toggle "Publish immediately"** if you want to save as draft
4. Click **"Add Blog Post"** to save

## 🎨 How Formatting is Converted

### Headings
```
Word Heading 1  →  <h3> (with Bootstrap classes)
Word Heading 2  →  <h4>
Word Heading 3  →  <h5>
```

### Text Formatting
```
Bold            →  <strong>
Italic          →  <em>
Underline       →  <u> (where supported)
```

### Lists
```
Bullet List     →  <ul class="mb-3"><li>...</li></ul>
Numbered List   →  <ol class="mb-3"><li>...</li></ol>
```

### Images
- Embedded images are converted to base64 data URIs
- Automatically made responsive with Bootstrap classes
- Alternative: Use header image field for main image

### Tables
```
Word Table      →  <table class="table table-bordered">
```

### Paragraphs
```
Regular text    →  <p class="mb-3">...</p>
```

## 🔄 Conversion Process

```
┌─────────────────┐
│  Upload .docx   │
│   file          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Mammoth.js     │
│  Conversion     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTML Cleanup   │
│  & Bootstrap    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preview        │
│  Display        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save to        │
│  Database       │
└─────────────────┘
```

## 💡 Tips & Best Practices

### For Best Results:

1. **Use Word Styles**
   - Use Heading 1, 2, 3 for sections
   - Don't manually resize text for headings
   - Apply styles from the Styles panel

2. **Image Optimization**
   - Compress images before inserting in Word
   - Recommended: 800px width for body images
   - Use PNG for graphics, JPG for photos

3. **Keep It Simple**
   - Avoid WordArt, text boxes, shapes
   - Use standard paragraph formatting
   - Stick to basic colors

4. **Test with Short Documents First**
   - Try with a 1-page document initially
   - Check how formatting converts
   - Adjust your Word template as needed

### Common Issues & Solutions

**Issue: Images not showing**
- Solution: Make sure images are embedded (not linked)
- Alternative: Use the header image field instead

**Issue: Formatting looks different**
- Solution: Use Word's built-in styles instead of manual formatting
- Check the HTML source tab to see exact conversion

**Issue: Complex tables not converting well**
- Solution: Simplify table structure, avoid merged cells
- Consider creating tables manually in HTML if needed

**Issue: Document conversion failed**
- Solution: Save as .docx (not .doc), ensure file isn't corrupted
- Try opening and re-saving in Word

## 📊 Supported vs. Unsupported Features

### ✅ Fully Supported
- Headings (1-3 levels)
- Paragraphs
- Bold, Italic, Underline
- Bullet lists
- Numbered lists
- Tables
- Images (embedded)
- Hyperlinks
- Text colors
- Blockquotes

### ⚠️ Partially Supported
- Complex tables (may need simplification)
- Multiple columns (converts to single column)
- Headers/Footers (ignored in conversion)
- Page breaks (ignored in web format)

### ❌ Not Supported
- WordArt
- SmartArt diagrams
- Text boxes
- Drawing shapes
- Equations (displayed as images)
- Embedded videos
- Macros
- Track changes

## 🔧 Advanced: Editing Generated HTML

If you need to make small edits after conversion:

1. Click the **"HTML Source"** tab in preview
2. Copy the HTML code
3. Switch content method to **"Write HTML"**
4. Paste and edit the HTML
5. Save normally

## 📖 Example Workflow

### Example: Creating a Teaching Tips Blog Post

1. **In Microsoft Word:**
   ```
   Heading 1: Top 5 AI Teaching Tips

   Paragraph: Introduction text here...

   Heading 2: Tip 1 - Use ChatGPT for Lesson Planning

   Paragraph: Detailed explanation...

   Bullet list:
   • Benefit 1
   • Benefit 2
   • Benefit 3

   [Insert image]

   Heading 2: Tip 2 - ...
   ```

2. **Save as** `teaching-tips.docx`

3. **In Admin Dashboard:**
   - Title: "Top 5 AI Teaching Tips"
   - Category: "Teaching Tools"
   - Date: Today
   - Upload header image
   - Upload DOCX: `teaching-tips.docx`
   - Review preview
   - Save!

4. **Generate Site** when ready

## 🆘 Troubleshooting

### Conversion taking too long?
- Large documents (50+ pages) may take 10-30 seconds
- Many images increase processing time
- Consider splitting into multiple posts

### Preview looks wrong?
- Check if you used manual formatting vs. Word styles
- Review HTML source for issues
- Try re-saving document in Word

### Getting error messages?
- Ensure file is `.docx` not `.doc`
- Try opening and re-saving in Word
- Check file isn't password protected
- Make sure file isn't corrupted

### Want to switch back to HTML?
- After upload, you can switch content method
- Your converted HTML will be in the HTML Source tab
- Copy and paste to manual HTML editor

## 📚 Additional Resources

- **Microsoft Word Help**: Learn about styles and formatting
- **HTML Basics**: Understanding the generated code
- **Bootstrap Documentation**: Understanding the styling classes

## 🎓 Learning Path

1. **Beginner**: Create simple posts with headings and paragraphs
2. **Intermediate**: Add images, lists, and basic tables
3. **Advanced**: Use styles consistently, optimize for web
4. **Expert**: Edit generated HTML for fine-tuning

---

**Pro Tip**: Create a Word template with your preferred styles and formatting, then use it for all blog posts to ensure consistency!
