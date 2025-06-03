import nibabel as nib

# Load the NIfTI file
img = nib.load('E:\MRI Research\motum-master\motum\sub-0001\anat\sub-0001_t2.nii.gz')

# Print the header
print(img.header)

print("Shape:", img.shape)
print("Spacing:", img.header.get_zooms())

# print slice thickness
print("Slice thickness:", img.header.get_zooms()[-1])
