# Shot List Editing Guide

## How to Edit Shot Lists for Future Updates

### 1. **File Location**
The shot lists are stored in: `templates/crew/scene_shots.html`

### 2. **Current Shot Lists**
- **Scene 10 (Mac Cottage Kitchen):** Lines 394-420
- **Scene 12 (Dominic Car Scene):** Lines 198-372

### 3. **Editing Process**

#### **Step 1: Find the Scene Section**
Look for the conditional statement:
```html
{% elif scene.scene_number == 10 %}
<!-- Mac Cottage Kitchen Scene -->
```

#### **Step 2: Update Shot Details**
Each shot is a table row with 6 columns:
- **Shot #:** Shot number
- **Description:** What's happening in the shot
- **Lens:** Camera lens specification
- **Framing:** How the shot is composed
- **Movement:** Camera movement type
- **Notes:** Additional technical notes

#### **Step 3: Example Shot Entry**
```html
<tr>
    <td>1</td>
    <td>Wide establishing</td>
    <td>Canon FD 24mm f/1.4 (38mm equivalent)</td>
    <td>Wide shot showing cramped kitchen, boxes, both characters</td>
    <td>Static on tripod, slightly high angle</td>
    <td>Deep focus showing the cluttered space</td>
</tr>
```

### 4. **Adding New Scenes**

#### **Step 1: Add Scene to Database**
```python
# In app.py, add new scene
new_scene = Scene(
    scene_number=15,
    title="New Scene Title",
    description="Scene description",
    location="Location name",
    time_of_day="DAY/NIGHT/DAWN/DUSK",
    scene_type="INT/EXT/INT-EXT",
    shot_count=5,  # Number of shots
    call_sheet_id=call_sheet_id  # Link to call sheet if scheduled
)
db.session.add(new_scene)
db.session.commit()
```

#### **Step 2: Add Shot List Template**
In `scene_shots.html`, add new conditional:
```html
{% elif scene.scene_number == 15 %}
<!-- New Scene Shot List -->
<div class="alert alert-info">
    <i class="fas fa-video"></i>
    <strong>Camera:</strong> RED KOMODO 6K |
    <strong>Lenses:</strong> Vintage Canon FD |
    <strong>Date:</strong> [DATE]
</div>
<div class="table-responsive">
    <table class="table table-striped">
        <!-- Shot list table here -->
    </table>
</div>
```

### 5. **Updating Morning Announcements**

#### **File Location**
`templates/crew/dashboard.html` - Lines 71-79

#### **Update Process**
Add new alert section:
```html
<div class="alert alert-success">
    <h5><i class="fas fa-video"></i> Updated Shot Lists for [DATE]</h5>
    <p class="mb-0">
        <strong>Scene Name:</strong> Description<br>
        <strong>Equipment:</strong> Camera and lens details<br>
        <strong>Location:</strong> Filming location and times
    </p>
</div>
```

### 6. **Technical Specifications Format**

#### **Lens Format**
- `Canon FD [focal length]mm f/[aperture] ([equivalent]mm equivalent)`
- Example: `Canon FD 50mm f/1.2 (80mm equivalent)`

#### **Movement Types**
- `Static` - No camera movement
- `Handheld` - Handheld camera work
- `Handheld, following` - Following subject
- `Static on tripod` - Tripod-mounted static shot

#### **Focus Notes**
- `Deep focus` - Everything in focus
- `Shallow DOF` - Shallow depth of field
- `Rack focus` - Focus changes during shot

### 7. **Best Practices**

1. **Consistency:** Use the same format for all shots
2. **Detail:** Include specific technical information
3. **Organization:** Group shots by location with table headers
4. **Testing:** Always test changes in the browser
5. **Backup:** Keep a backup of working versions

### 8. **Quick Reference**

#### **Common Lens Specifications**
- `Canon FD 24mm f/1.4 (38mm equivalent)` - Wide establishing
- `Canon FD 50mm f/1.2 (80mm equivalent)` - Standard coverage
- `Canon FD 85mm f/1.8 (136mm equivalent)` - Close-ups
- `Canon FD 35mm f/2 (56mm equivalent)` - Two-shots

#### **Common Movement Types**
- `Static` - Locked off
- `Handheld` - Handheld
- `Handheld, following` - Following action
- `Static on tripod` - Tripod mounted

### 9. **Troubleshooting**

#### **If shots don't appear:**
1. Check scene number matches database
2. Verify conditional statement syntax
3. Check table structure is complete

#### **If formatting breaks:**
1. Ensure all `<tr>` tags are closed
2. Check table structure matches header
3. Verify HTML syntax

### 10. **Contact for Help**
For technical issues or questions about shot list editing, refer to the development team or check the morning announcements for updates.
