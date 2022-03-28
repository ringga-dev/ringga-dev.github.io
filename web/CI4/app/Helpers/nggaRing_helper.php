<?php

/**
 * fungsi ketika user yang telah terdaftar di sistem akan mengakses api server
 * @param string $username
 * @param string $password
 * jika akses user tersebut berhasil maka akan mengembalikan token yang akan di gunakan untuk autentikasi 
 * user ke server api
 */
function getToken($badge_id)
{
    $db = \Config\Database::connect();
    $key = $db->table('mas_user_token')->where(['badge_id' => $badge_id])->get()->getRowArray();
    if ($key) {
        $db->table('mas_user_token')->update(['exp_token' => time()]);
        $data = $db->table('mas_user_token')->where(['badge_id' => $badge_id])->get()->getRowArray();
    } else {
        $data = [
            'badge_id' => $badge_id, //pemilik token
            'token_app' => preg_replace("/[^a-zA-Z0-9]/", "", password_hash(bin2hex(openssl_random_pseudo_bytes(64)), PASSWORD_BCRYPT)), //create token
            'exp_token' => time(), //waktu token di buat
            'exp_time' => "0" // merupakan waktu yang akan di set untuk mengaktifkan token 
        ];

        $db->table('mas_user_token')->insert($data);

        $data = $db->table('mas_user_token')->where(['badge_id' => $badge_id])->get()->getRowArray();
    }

    return $data['token_app'];
}
