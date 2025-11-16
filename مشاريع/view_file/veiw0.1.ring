# Project: File Content Viewer
# Author: Your Name
# Date: 2023-11-20

load "guilib.ring"
load "stdlib.ring"

// Global variables
contentLayout = NULL
currentFileType = ""

new qApp {
    // Create main window
    win1 = new qWidget() {
        setWindowTitle("File Content Viewer")
        setGeometry(100, 100, 800, 600)
        setStyleSheet("background-color: #f0f0f0;")

        // Create layout
        layout = new qVBoxLayout() {
            // Title
            labelTitle = new qLabel(win1) {
                setText("File Content Viewer")
                setAlignment(Qt_AlignHCenter)
                setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin: 20px;")
            }
            addwidget(labelTitle)
            

            // File selection section
            
                
                
                    textFilePath = new qLineEdit(win1) {
                        setPlaceholderText("Select a file...")
                        setReadOnly(True)
                    }
                    addwidget(textFilePath)
                    btnBrowse = new qPushButton(win1) {
                        setText( "Browse" )
                        setStyleSheet("
                            QPushButton {
                                background-color: #4CAF50;
                                color: white;
                                border: none;
                                padding: 8px 16px;
                                border-radius: 4px;
                            }
                            QPushButton:hover {
                                background-color: #45a049;
                            }
                        ")
                    }
                    addwidget(btnBrowse)
                
            

            // Content display area
            groupContent = new qVBoxLayout() {
               // setTitle("File Content")
                addLayout(new qVBoxLayout())
              //  setMinimumHeight(400)
            }
            addLayout(groupContent)
            // Status bar
            labelStatus = new qLabel(win1) {
                setText("Please select a file to view its content")
                setStyleSheet("color: #666; padding: 10px;")
            }
            addwidget(labelStatus)
        }

        // Connect events
        btnBrowse.setclickEvent("btnBrowse_clicked()")
    }
    displayFileContent("/home/hassan2harby/hassan document/whatapp backup 25 11/Media/WhatsApp Images/IMG-20251102-WA0125.jpg")
win1.setLayout(layout)
    win1.show()
    exec()
}



func btnBrowse_clicked
    fileName=""
    // Open file dialog
    new qfiledialog(win1) {fileName=getopenfilename(win1, "Select File", "", 
                           "All Files (*.*);;Text Files (*.txt);;Image Files (*.png *.jpg *.bmp);;Sound Files (*.wav *.mp3)")
                           }
    
    if fileName != ""
        textFilePath.setText(fileName)
        displayFileContent(fileName)
    ok

func displayFileContent(fileName)
    // Clear previous content
    if contentLayout != NULL
        contentLayout.delete()
    ok
    
    contentLayout = new qVBoxLayout()
    groupContent.addLayout(contentLayout)
    
    // Get file extension
    fileExt = lower(getFileExtension(fileName))
    see fileExt
    // Display based on file type
    switch fileExt
    on ".txt"
        displayTextFile(fileName)
    on  ".jpg" ".png" ".jpeg" ".bmp" ".gif"
        displayImageFile(fileName)
    on ".wav" ".mp3" ".ogg"
        displaySoundFile(fileName)
    other
        displayUnknownFile(fileName)
    off
    
    currentFileType = fileExt

func displayTextFile(fileName)
    try
        content = read(fileName)
        textEdit = new qTextEdit() {
            setPlainText(content)
            setReadOnly(True)
            setStyleSheet("
                QTextEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 10px;
                    font-family: 'Courier New';
                }
            ")
        }
        contentLayout.addWidget(textEdit)
        labelStatus.setText("Text file loaded successfully - " + string(len(content)) + " characters")
    catch
        labelStatus.setText("Error reading text file")
    end

func displayImageFile(fileName)
   // try
        // Create image label
        labelImage = new qLabel(win1) {
            setAlignment(Qt_AlignHCenter)
            setStyleSheet("background-color: white; border: 1px solid #ccc;")
        }
        
        // Load and scale image
        pixmap = new qPixmap(fileName)
        if !pixmap.isNull()
            // Scale image to fit while maintaining aspect ratio
            scaledPixmap = pixmap.scaled(600, 400, 0, 0)
            labelImage.setPixmap(scaledPixmap)
            contentLayout.addWidget(labelImage)
            
            // Show image info
            infoLabel = new qLabel(win1) {
                setText("Image: " + string(pixmap.width()) + "x" + string(pixmap.height()) + 
                       " | Format: " + getFileExtension(fileName))
                setAlignment(Qt_AlignHCenter)
                setStyleSheet("color: #666; margin: 10px;")
            }
            contentLayout.addWidget(infoLabel)
            
            labelStatus.setText("Image loaded successfully")
        else
            throw("Failed to load image")
        ok
 //   catch
 //       errorLabel = new qLabel(win1)
 //       errorLabel.setText("Error loading image file")
 //       errorLabel.setAlignment(Qt_AlignHCenter)
 //       contentLayout.addWidget(errorLabel)
 //       labelStatus.setText("Error loading image file")
 //   end

func displaySoundFile(fileName)
    try
        // Sound file information
        groupInfo = new qGroupBox() {
            setTitle("Sound Information")
            setLayout(new qVBoxLayout() {
                addWidget(new qLabel("File: " + fileName))
                addWidget(new qLabel("Type: " + getFileExtension(fileName)))
                addWidget(new qLabel("Sound files can be played using external applications"))
            })
        }
        contentLayout.addWidget(groupInfo)
        
        // Play button (conceptual - would need sound library for actual playback)
        btnPlay = new qPushButton("🎵 Play Sound (External)") {
            setStyleSheet("
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 6px;
                    font-size: 16px;
                    margin: 20px;
                }
                QPushButton:hover {
                    background-color: #0b7dda;
                }
            ")
        }
        contentLayout.addWidget(btnPlay)
        
        // Connect play button (this would open in external player)
        btnPlay.setclickEvent(func (fileName){
            // This would typically use a sound library
            // For now, just show a message
            labelStatus.setText("Sound playback would require additional libraries")
        })
        
        labelStatus.setText("Sound file information displayed")
    catch
        labelStatus.setText("Error processing sound file")
    end

func displayUnknownFile(fileName)
    labelUnknown = new qLabel(win1) {
        setText("Unsupported file type: " + getFileExtension(fileName) + 
               "\n\nThis viewer supports:\n" +
               "• Text files (.txt)\n" +
               "• Image files (.png, .jpg, .bmp, .gif)\n" +
               "• Sound files (.wav, .mp3, .ogg)")
        setAlignment(Qt_AlignHCenter)
        setStyleSheet("
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 20px;
                margin: 10px;
                color: #856404;
            }
        ")
    }
    contentLayout.addWidget(labelUnknown)
    labelStatus.setText("Unsupported file type")

// Utility functions
func getFileExtension(fileName)
    return right(fileName, 4)  // Simple extension extraction

func read(fileName)
    fp = fopen(fileName, "r")
    content = ""
    if fp
        while not feof(fp)
            content += fgetc(fp)
        end
        fclose(fp)
    ok
    return content
