PROVIDER_CONFIGS = {
    "google": {
        "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
        "client_kwargs": {"scope": "openid email profile"}
    },
    # "kakao": {
    #     "authorize_url": "https://kauth.kakao.com/oauth/authorize",
    #     "access_token_url": "https://kauth.kakao.com/oauth/token",
    #     "userinfo_endpoint": "https://kapi.kakao.com/v2/user/me",
    #     "api_base_url": "https://kapi.kakao.com",
    #     "client_kwargs": {"scope": "account_email profile_nickname"}
    # },
    # "naver": {
    #     "authorize_url": "https://nid.naver.com/oauth2.0/authorize",
    #     "access_token_url": "https://nid.naver.com/oauth2.0/token",
    #     "userinfo_endpoint": "https://openapi.naver.com/v1/nid/me",
    #     "api_base_url": "https://openapi.naver.com",
    #     "client_kwargs": {"scope": "name email"}
    # },
    # "github": {
    #     "authorize_url": "https://github.com/login/oauth/authorize",
    #     "access_token_url": "https://github.com/login/oauth/access_token",
    #     "userinfo_endpoint": "https://api.github.com/user",
    #     "api_base_url": "https://api.github.com/",
    #     "client_kwargs": {"scope": "read:user user:email"}
    # }
}
