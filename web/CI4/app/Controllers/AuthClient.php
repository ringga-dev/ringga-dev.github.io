<?php

namespace App\Controllers;

use CodeIgniter\RESTful\ResourceController;

use App\Models\RestApiModel;
use CodeIgniter\API\ResponseTrait;

class AuthClient extends ResourceController
{
    use ResponseTrait;
    public function __construct()
    {
        $this->model = new RestApiModel();
        helper(['api', 'form', 'security', 'nggaRing']);
    }

    public function index()
    {
        /**
         * fungsi ketika user melakukan login di aplikasi
         * dengan mengirimkan username dan password
         */

        $badge_id = $this->request->getPost('badge_id');
        $password = $this->request->getPost('password');
        $data = $this->model->loginUser($badge_id, $password);
        if ($data['stts'] == true) {
            unset($data['data']['password']);
            $data = [
                'stts' => true,
                'msg' => 'Login Success',
                'data' => $data['data'] + ['token' => getToken($data['data']['badge_id'])]
            ];
            return $this->respond($data, 200);
        } else {
            return $this->respond($data, 403);
        }
    }

    public function register()
    {
        $data = [
            'badge_id' => $this->request->getPost('badge_id'),
            'name' => $this->request->getPost('name'),
            'email' => $this->request->getPost('email'),
            'password' => password_hash($this->request->getPost('password'), PASSWORD_BCRYPT),
            'image' => $this->request->getPost('image'),
            'alamat' => $this->request->getPost('alamat'),
            'jabatan' => $this->request->getPost('jabatan'),
            'nik' => $this->request->getPost('nik'),
            'number_phone' => $this->request->getPost('number_phone'),
            'created' => date('Y-M-d h:i:s A') . ' by ' . $this->request->getPost('name')
        ];

        $data = $this->model->registerUser($data);
        if ($data['stts'] == true) {
            $data = [
                'stts' => true,
                'msg' => $data['msg']
            ];
            return $this->respond($data, 300);
        } else {
            $data = [
                'stts' => false,
                'msg' => $data['msg']
            ];
            return $this->respond($data, 300);
        }
    }
}
