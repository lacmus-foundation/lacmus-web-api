using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace Identity.ViewModels.Token
{
    public class AccessToken : IToken, IAccessToken, IInfoToken
    {
        [JsonPropertyName("aud")]
        public string Aud { get; set; }
        [JsonPropertyName("iss")]
        public string Iss { get; set; }
        [JsonPropertyName("sub")]
        public string Sub { get; set; }
        [JsonPropertyName("jti")]
        public string Jti { get; set; }
        [JsonPropertyName("roles")]
        public IEnumerable<string> Roles { get; set; }
        [JsonPropertyName("exp")]
        public int Exp { get; set; }
    }
}