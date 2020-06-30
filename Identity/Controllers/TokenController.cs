using Identity.ViewModels.Token;
using Identity.ViewModels.UserLogin;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Identity.Controllers
{
    [Route("api/v1/token")]
    [ApiController]
    public class TokenController : Controller
    {
/* TODO: user login
    look at https://www.krakend.io/docs/authorization/jwt-signing/
            https://ru.wikipedia.org/wiki/JSON_Web_Token

    curl -X POST --data '{"email":"gosha20777@lacmus.org","password":"pass"}' https://api.lacmus.org/api/v1/token
        {
            "access_token": {
                "aud": "https://api.lacmus.org",
                "iss": "https://api.lacmus",
                "sub": "1234567890qwertyuio",
                "jti": "mnb23vcsrt756yuiomnbvcx98ertyuiop",
                "roles": ["user", "admin"],
                "exp": 1735689600
            },
            "refresh_token": {
                "aud": "https://api.lacmus.org",
                "iss": "https://api.lacmus",
                "sub": "1234567890qwertyuio",
                "jti": "mnb23vcsrt756yuiomn12876bvcx98ertyuiop",
                "exp": 1735689600
            },
            "exp": 1735689600
        }
iss: чувствительная к регистру строка или URI, которая является уникальным идентификатором стороны, генерирующей токен (issuer).
sub: чувствительная к регистру строка или URI, которая является уникальным идентификатором стороны, о которой содержится информация в данном токене (subject). Значения с этим ключом должны быть уникальны в контексте стороны, генерирующей JWT.
aud: массив чувствительных к регистру строк или URI, являющийся списком получателей данного токена. Когда принимающая сторона получает JWT с данным ключом, она должна проверить наличие себя в получателях — иначе проигнорировать токен (audience).
exp: время в формате Unix Time, определяющее момент, когда токен станет не валидным (expiration).
jti: строка, определяющая уникальный идентификатор данного токена (JWT ID) == session id.
*/
        [HttpPost]
        [AllowAnonymous]
        public ActionResult<TokenIssuer> GetToken([FromBody] LoginViewModel model)
        {
            var exp = 1735689600;
            var aud = "https://lacmus.io";
            var iss = "https://lacmus";
            var sub = "1234567890qwertyuio";
            var jti = "mnb23vcsrt756yuiomnbvcx98ertyuiop";
            var roles = new [] { "user", "admin" };
            
            var tokenIssuer = new TokenIssuer();
            tokenIssuer.AccessToken = new AccessToken();
            tokenIssuer.Exp = exp;
            tokenIssuer.AccessToken.Aud = aud;
            tokenIssuer.AccessToken.Iss = iss;
            tokenIssuer.AccessToken.Sub = sub;
            tokenIssuer.AccessToken.Jti = jti;
            tokenIssuer.AccessToken.Roles = roles;
            tokenIssuer.AccessToken.Exp = exp;
            return tokenIssuer;
        }
    }
}