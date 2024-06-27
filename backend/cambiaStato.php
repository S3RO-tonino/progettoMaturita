<?php
    $filepath = 'config.json';

    // Leggere il contenuto del file JSON
    $jsonString = file_get_contents($filepath);

    if ($jsonString === false) {
        die('Errore nella lettura del file JSON');
    }

    // JSON -> Array
    $data = json_decode($jsonString, true);

    if ($data === null && json_last_error() !== JSON_ERROR_NONE) {
        die('Errore nella decodifica del file JSON');
    }

    if $data['status'] === true:{
        $data['status'] = false;
    }
    else{
        $data['status'] = true;
    }

    // Array -> JSON
    $newJsonString = json_encode($data, JSON_PRETTY_PRINT);

    if ($newJsonString === false) {
        die('Errore nella codifica dei dati JSON');
    }

    // Modifica del file
    $result = file_put_contents($filepath, $newJsonString);

    if ($result === false) {
        die('Errore nella scrittura del file JSON');
    }
?>