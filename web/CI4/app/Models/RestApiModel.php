<?php

namespace App\Models;

use CodeIgniter\Model;

class RestApiModel extends Model
{

    public function loginUser($badge_id, $password)
    {
        $data = $this->db->table('mas_user_data')->where(['badge_id' => $badge_id])->get()->getRowArray();
        if (!$data) {
            return [
                'stts' => false,
                'msg' => 'User not found'
            ];
        } else {
            if (password_verify($password, $data['password'])) {
                return [
                    'stts' => true,
                    'msg' => 'Login Success',
                    'data' => $data
                ];
            } else {
                return [
                    'stts' => false,
                    'msg' => 'Wrong Password'
                ];
            }
        }
    }

    public function registerUser($data)
    {
        $badge = $this->db->table('mas_user_data')->where(['badge_id' => $data['badge_id']])->get()->getRowArray();
        $email = $this->db->table('mas_user_data')->where(['email' => $data['email']])->get()->getRowArray();
        $nik = $this->db->table('mas_user_data')->where(['nik' => $data['nik']])->get()->getRowArray();
        $number_phone = $this->db->table('mas_user_data')->where(['number_phone' => $data['number_phone']])->get()->getRowArray();

        if ($badge) {
            $data = [
                'stts' => false,
                'msg' => 'badge already registered'
            ];
        } elseif ($email) {
            $data = [
                'stts' => false,
                'msg' => 'email already registered'
            ];
        } elseif ($nik) {
            $data = [
                'stts' => false,
                'msg' => 'nik already registered'
            ];
        } elseif ($number_phone && $data['number_phone']) {
            $data = [
                'stts' => false,
                'msg' => 'number phone already registered'
            ];
        } else {
            $this->db->table('mas_user_data')->insert($data);
            $data = [
                'stts' => true,
                'msg' => 'user registered successfully'
            ];
        }
        return $data;
    }
}
