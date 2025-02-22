<?php
$servername = "localhost"; // Change if using a different server
$username = "root"; // MySQL username
$password = "9598200!@#$%^&*("; // MySQL password
$database = "student"; // Database name

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $full_name = $_POST['full_name'];
    $service_required = $_POST['service'];
    $custom_service = isset($_POST['custom_service']) ? $_POST['custom_service'] : '';
    $email = $_POST['email'];
    $phone = $_POST['phone'];
    $address = $_POST['address'];
    $password = password_hash($_POST['password'], PASSWORD_BCRYPT); // Encrypt password
    $gender = $_POST['gender'];

    $sql = "INSERT INTO users (full_name, service_required, custom_service, email, phone, address, password, gender) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)";

    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssssssss", $full_name, $service_required, $custom_service, $email, $phone, $address, $password, $gender);

    if ($stmt->execute()) {
        echo "<script>alert('Registration Successful!'); window.location.href='index.php';</script>";
    } else {
        echo "Error: " . $stmt->error;
    }
    
    $stmt->close();
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Form</title>
    <link rel="stylesheet" href="styles2.css">
</head>
<body>
    <div class="container">
        <div class="title">Contact</div>
        <div class="content">
            <form action="" method="POST">
                <div class="user-details">
                    <div class="input-box">
                        <span class="details">Full Name</span>
                        <input type="text" name="full_name" placeholder="Enter your name" required>
                    </div>
                    <div class="form-item">
                        <label for="service">Service Required:</label>
                        <select id="service" name="service" required>
                            <option value="web-development">Web Development</option>
                            <option value="app-development">App Development</option>
                            <option value="video-editing">Video Editing</option>
                            <option value="seo-services">SEO Services</option>
                            <option value="graphic-design">Graphic Design</option>
                            <option value="content-writing">Content Writing</option>
                            <option value="other">Other</option>
                        </select>
                        <input type="text" name="custom_service" placeholder="Specify if other">
                    </div>
                    <div class="input-box">
                        <span class="details">Email</span>
                        <input type="email" name="email" placeholder="Enter your email" required>
                    </div>
                    <div class="input-box">
                        <span class="details">Phone Number</span>
                        <input type="text" name="phone" placeholder="Enter your number" required>
                    </div>
                    <div class="input-box">
                        <span class="details">Address</span>
                        <input type="text" name="address" placeholder="Enter your address" required>
                    </div>
                    <div class="input-box">
                        <span class="details">Password for Uniqueness</span>
                        <input type="password" name="password" placeholder="For New ID Proof" required>
                    </div>
                </div>
                <div class="gender-details">
                    <span class="gender-title">Gender</span>
                    <div class="category">
                        <input type="radio" name="gender" id="dot-1" value="Male" required>
                        <label for="dot-1"><span class="dot one"></span><span class="gender">Male</span></label>
                        
                        <input type="radio" name="gender" id="dot-2" value="Female" required>
                        <label for="dot-2"><span class="dot two"></span><span class="gender">Female</span></label>
                        
                        <input type="radio" name="gender" id="dot-3" value="Prefer not to say" required>
                        <label for="dot-3"><span class="dot three"></span><span class="gender">Prefer not to say</span></label>
                    </div>
                </div>
                <div class="button">
                    <input type="submit" value="Register">
                </div>
                <div class="back-button">
                    <button type="button" onclick="window.history.back();">Back</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
