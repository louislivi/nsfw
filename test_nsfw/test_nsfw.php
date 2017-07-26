<?php

function return_result($filename,$filesize=0){
  $path = $filename;
  if ($filesize) {
    $result_data['Size'] = $filesize;
  }else{
    $result_data['Type'] = $_FILES["file"]["type"];
    $result_data['Size'] = ($_FILES["file"]["size"] / 1024);
  }
  $score_result  = exec("curl localhost:8888/alisa?filename=".$path);
  $match_count = preg_match_all('/score:(.*)/',$score_result,$matches);
  if ($match_count > 0) {
    $result_data['Score'] = strip_tags(trim($matches[1][0]));
    $result_data['Error'] = 0;
    if ($result_data['Score'] >= 0.4) {
      $result_data['Status'] = '性感';
    }elseif ($result_data['Score'] >= 0.9) {
      $result_data['Status'] = '色情';
    }else{
      $result_data['Status'] = '正常';
    }
  }else{
    $result_data['Score'] = 0;
    $result_data['Error'] = $score_result;
    $result_data['Status'] = '错误';
  }
  return json_encode($result_data);
}

if ($_POST['img_url'] && $_POST['type'] == 0) {
  $url = $_POST['img_url'];
  $hdrs = @get_headers($url);
  $is_url = is_array($hdrs) ? preg_match('/^HTTP\\/\\d+\\.\\d+\\s+2\\d\\d\\s+.*$/',$hdrs[0]) : false;
  if ($is_url) {
     $content  = file_get_contents($url);
     $filesize = strlen($content)/1024;
     $filename = date('YmdHis').mt_rand(1000,9999).'.jpg';
	   file_put_contents('../upload/'.$filename, $content);
     echo return_result($filename,$filesize);
  }
}elseif ($_POST['img_url'] && $_POST['type'] == 1) {
     $url = $_POST['img_url'];
     $content  = file_get_contents($url);
     $filesize = strlen($content)/1024;
     $filename = basename($url);
     echo return_result($filename,$filesize);
}elseif (//(($_FILES["file"]["type"] == "image/gif")||
(($_FILES["file"]["type"] == "image/jpeg")
|| ($_FILES["file"]["type"] == "image/bmp")
|| ($_FILES["file"]["type"] == "image/png")
|| ($_FILES["file"]["type"] == "image/pjpeg"))
&& ($_FILES["file"]["size"] < 2097152))
  {
  if ($_FILES["file"]["error"] > 0)
    {
    echo json_encode(array('Error'=> "Return Code: " . $_FILES["file"]["error"]));
    }
  else
    {
      $filename = date('YmdHis').mt_rand(1000,9999).'.jpg';
      $result = move_uploaded_file($_FILES["file"]["tmp_name"],
      "../upload/" . $filename);
      if($result){
        echo return_result($filename);
      }
    }
  }
else
  {
    echo json_encode(array('Error'=>"图片不得大于2M,仅支持PNG、JPG、jpeg、BMP图片文件。"));
  }
?>
