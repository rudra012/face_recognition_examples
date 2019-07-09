import os

import face_recognition
from PIL import Image, ImageDraw

#  Create arrays of encodings and names
known_face_encodings = []
known_face_names = []

# Iterate over known images
directory = './img/known/'

for filename in os.listdir(directory):
    if len(filename.split('.')) == 2:
        name, ext = filename.split('.')
        if ext in ['jpg', 'png']:
            image = face_recognition.load_image_file(directory + filename)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

print(f'There are {len(known_face_names)} known people')

# Load test image to find faces in
test_image = face_recognition.load_image_file(
    './img/groups/bill-steve-elon.jpg')

# Find faces in test image
face_locations = face_recognition.face_locations(test_image)
face_encodings = face_recognition.face_encodings(test_image, face_locations)

# Convert to PIL format
pil_image = Image.fromarray(test_image)

# Create a ImageDraw instance
draw = ImageDraw.Draw(pil_image)

# Loop through faces in test image
for (top, right, bottom, left), face_encoding in zip(face_locations,
                                                     face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings,
                                             face_encoding)

    name = "Unknown Person"

    # If match
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    # Draw box
    draw.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0))

    # Draw label
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)),
                   fill=(255, 255, 0), outline=(255, 255, 0))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(0, 0, 0))

del draw

# Display image
pil_image.show()

# Save image
# pil_image.save('identify.jpg')
